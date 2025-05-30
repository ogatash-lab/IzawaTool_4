import yaml
import pandas as pd
import os
import glob
import re
import copy

import izawa_cunfusion_matrix

# YAMLファイルのパスを指定
ideal_file_path = "../izawa_result/cmd_kiki_none.yaml"
#ideal_file_path = "../izawa_result/cmd_kiki_temp.yaml"
verification_file_path = "B/cost-cost"  # ディレクトリ例

# YAMLファイルを読み込み
def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# 特定のroute以下の要素を取得する関数
def get_elements_below_route(data, target_route):
    current_level = data
    try:
        for key in target_route:
            current_level = current_level[key]
        return current_level
    except KeyError:
        return None

def dict_to_dataframe(data):
    # 省略を回避するための pandas オプション設定
    pd.set_option('display.max_rows', None)      # 表示する最大行数を制限なしに
    pd.set_option('display.max_columns', None)   # 表示する最大列数を制限なしに
    pd.set_option('display.max_colwidth', None)  # 列の最大幅を無制限に
    pd.set_option('display.width', 1000)         # 出力の横幅を大きめに

    row_labels = ["Cf1","Cf2","Cf3","Cf4","Cf5","Cf6","Cf7","Cf8","Cf9"]
    df = pd.DataFrame(data, index=row_labels)

    # 各行の値を合計する列を追加 (axis=1 で行方向に合計)
    df["Total"] = df.sum(axis=1)

    return df

def compare_states(ideal_state, verification_state):
    DOWN = 0
    MISS = 0

    for ideal in ideal_state:
        vlan_ideal, id_ideal, state_ideal = ideal  # 3つの要素を変数に展開

        # verification_state に (vlan_ideal, id_ideal) が含まれる要素を検索
        matched_item = None
        for ver in verification_state:
            vlan_ver, id_ver, state_ver = ver
            if vlan_ideal == vlan_ver and id_ideal == id_ver:
                matched_item = ver
                break

        # 見つからない場合
        if not matched_item:
            MISS += 1
        else:
            # 3番目の要素(状態)を比較
            if state_ideal != state_ver:
                if state_ver == "DOWN":
                    DOWN += 1

    return [DOWN, MISS]

# リストを比較する関数
def compare_routes(ideal_route, verification_route, result_table):
    suspect_device = []

    # verification_routeの最後の要素が"Cf"を含む場合、その要素をsuspect_deviceに追加して終了
    #if ideal_route != verification_route and "Cf" in verification_route[-1]:
    if False:
        suspect_device.append(verification_route[-1])
    else:
        max_length = max(len(ideal_route), len(verification_route))
        for i in range(max_length):
            ideal = ideal_route[i] if i < len(ideal_route) else "(None)"
            verify = verification_route[i] if i < len(verification_route) else "(None)"
            if ideal != verify and i > 0:
                suspect_device.append(ideal_route[i - 1])
                break

        # ideal_route に含まれるが verification_route に含まれない "Cf" を含む要素を追加
        missing_in_verification = set(ideal_route) - set(verification_route)
        suspect_device.extend([device for device in missing_in_verification if "Cf" in device])

    # result_table に suspect_device の要素を反映
    for device in suspect_device:
        if device in result_table:
            result_table[device] += 1


if __name__ == "__main__":

    AUC_data = {}

    #上位何機器をサジェストするか
    for k in range(10):
    #for k in [1]:

        #重みづけなし
        #neighbor_devices = {"Cf1":["Cf1"], "Cf2":["Cf2"], "Cf3":["Cf3"], "Cf4":["Cf4"], "Cf5":["Cf5"], "Cf6":["Cf6"], "Cf7":["Cf7"], "Cf8":["Cf8"], "Cf9":["Cf9"]}

        #自分＋ネイバー 2-6結線
        neighbor_devices = {"Cf1":["Cf1","Cf2"], "Cf2":["Cf2","Cf1","Cf3","Cf9","Cf6"], "Cf3":["Cf3","Cf2","Cf4"], "Cf4":["Cf4","Cf3","Cf5"], "Cf5":["Cf5","Cf4","Cf6"], "Cf6":["Cf6","Cf5","Cf7","Cf2"], "Cf7":["Cf7","Cf6","Cf8"], "Cf8":["Cf8","Cf7","Cf9"], "Cf9":["Cf9","Cf8","Cf2"]}

        #自分＋ネイバー
        #neighbor_devices = {"Cf1":["Cf1","Cf2"], "Cf2":["Cf2","Cf1","Cf3","Cf9"], "Cf3":["Cf3","Cf2","Cf4"], "Cf4":["Cf4","Cf3","Cf5"], "Cf5":["Cf5","Cf4","Cf6"], "Cf6":["Cf6","Cf5","Cf7"], "Cf7":["Cf7","Cf6","Cf8"], "Cf8":["Cf8","Cf7","Cf9"], "Cf9":["Cf9","Cf8","Cf2"]}

        #ネイバーのみ
        #neighbor_devices = {"Cf1":["Cf2"], "Cf2":["Cf1","Cf3","Cf9","Cf6"], "Cf3":["Cf2","Cf4"], "Cf4":["Cf3","Cf5"], "Cf5":["Cf4","Cf6"], "Cf6":["Cf5","Cf7","Cf2"], "Cf7":["Cf6","Cf8"], "Cf8":["Cf7","Cf9"], "Cf9":["Cf8","Cf2"]}

        # YAMLデータをロード
        ideal_data = load_yaml(ideal_file_path)

        # verification_file_path がディレクトリかファイルかを判定
        if os.path.isdir(verification_file_path):
            # ディレクトリ内の .yaml ファイルをすべて取得
            yaml_files = glob.glob(os.path.join(verification_file_path, "*.yaml"))
        else:
            # 1つのファイルのみをリスト化
            yaml_files = [verification_file_path]

        confusion_matrix = {"TP": 0, "TN": 0, "FP": 0, "FN": 0}

        # ファイルごとに処理
        for vf_path in yaml_files:
            print(f"\n===== Verification file: {vf_path} =====")
            verification_data = load_yaml(vf_path)

            # ファイル名から機器名 (Cf + 数字) を抽出し、列名に使う
            # 複数マッチする場合は「_」で結合して1つの列ラベルとする
            pattern = r"(Cf\d+)"
            error_device_list = re.findall(pattern, vf_path)
            device_label = "_".join(error_device_list) if error_device_list else "NoDeviceFound"

            # ここから各top_keyごとのDOWN/MISSを集計
            DOWN_result_table = {}
            MISS_result_table = {}
            TRACE_result_table = {}

            for top_key in ideal_data.keys():
                neighbor_relationship = copy.deepcopy(neighbor_devices)

                if "-" in top_key:
                    device1, device2 = top_key.split("-")

                    # device1のリストからdevice2を削除
                    if device2 in neighbor_relationship.get(device1, []):
                        neighbor_relationship[device1].remove(device2)

                    # device2のリストからdevice1を削除
                    if device1 in neighbor_relationship.get(device2, []):
                        neighbor_relationship[device2].remove(device1)

                DOWN_table = {"Cf1": 0, "Cf2": 0, "Cf3": 0, "Cf4": 0, "Cf5": 0, "Cf6": 0, "Cf7": 0, "Cf8": 0, "Cf9": 0}
                MISS_table = {"Cf1": 0, "Cf2": 0, "Cf3": 0, "Cf4": 0, "Cf5": 0, "Cf6": 0, "Cf7": 0, "Cf8": 0, "Cf9": 0}

                target_route = [top_key, 'ospf']
                ideal_elements = get_elements_below_route(ideal_data, target_route)
                verification_elements = get_elements_below_route(verification_data, target_route)

                if ideal_elements is None or verification_elements is None:
                    continue

                for key in ideal_elements.keys():
                    if key not in verification_elements:
                        state = compare_states(ideal_elements[key], [])
                    else:
                        state = compare_states(ideal_elements[key], verification_elements[key])

                    for neighbor in neighbor_relationship[key]:
                        DOWN_table[neighbor] += state[0]
                    MISS_table[key] += state[1]

                # row_labels の並び順でリスト化し DataFrame で使える形に
                DOWN_result_table[top_key] = list(DOWN_table.values())
                MISS_result_table[top_key] = list(MISS_table.values())

            #################トレースルート###################
            for top_key in ideal_data.keys():
                # 対象のrouteを指定
                target_route = [top_key, 'communication-route']

                # ファイルごとの結果テーブルを初期化 (行→Cf1..Cf9)
                trace_table = {"Cf1": 0, "Cf2": 0, "Cf3": 0, "Cf4": 0, "Cf5": 0, "Cf6": 0, "Cf7": 0, "Cf8": 0, "Cf9": 0}

                # 理想状態と実際の状態のデータを取得
                ideal_elements = get_elements_below_route(ideal_data, target_route)
                verification_elements = get_elements_below_route(verification_data, target_route)

                # 該当要素が辞書であることを確認
                if isinstance(ideal_elements, dict) and isinstance(verification_elements, dict):
                    for key in ideal_elements:
                        if key in verification_elements:
                            ideal_route = ideal_elements[key].get('icmp', [])
                            verification_route = verification_elements[key].get('icmp', [])
                            compare_routes(ideal_route, verification_route, trace_table)
                else:
                    print("Error: One or both routes do not contain dictionaries of elements.")

                # top_key ごとに結果を入れる (行= Cf1..Cf9)
                TRACE_result_table[top_key] = list(trace_table.values())

            miss_df = dict_to_dataframe(MISS_result_table)
            down_df = dict_to_dataframe(DOWN_result_table)
            trace_df = dict_to_dataframe(TRACE_result_table)

            if True:
                print("\n[ERROR result for this file]")
                print(miss_df["Total"])

                print("\n[DOWN result for this file]")
                print(down_df["Total"])

                print("\n[TRACE result for this file]")
                print(trace_df["Total"])

                print()

            message_file = ""
            prediction_device_list = []
            # 「MISS」シナリオ
            if miss_df["Total"].sum() != 0:
                message_file = "error_message.txt"
                print("ERROR exists!!!")
                print("Required interface does not exist")

                # ---- ここから変更 ----
                primary_series = miss_df["Total"]      # メインのスコア: MISS
                secondary_series = trace_df["Total"]   # タイブレーク用: TRACE

                # 複合スコア = primary * (十分大きい係数) + secondary
                # こうすることで primary が同点の場合に secondary が大きい方を優先
                combined_score = primary_series * 10000 + secondary_series

                # 降順にソート
                combined_score = combined_score.sort_values(ascending=False)

                # 上位k件（ただし ties を排除）
                prediction_device_list = list(izawa_cunfusion_matrix.topk_excluding_ties(combined_score, k))
                # ---- ここまで変更 ----

            # 「DOWN」シナリオ
            elif down_df["Total"].sum() != 0:
                message_file="down_message.txt"
                print("DOWN exists!!!")
                print("Neighbor relationship not established.")

                # ---- ここから変更 ----
                primary_series = down_df["Total"]      # メインのスコア: DOWN
                secondary_series = trace_df["Total"]   # タイブレーク用: TRACE

                combined_score = primary_series * 10000 + secondary_series
                combined_score = combined_score.sort_values(ascending=False)

                prediction_device_list = list(izawa_cunfusion_matrix.topk_excluding_ties(combined_score, k))
                # ---- ここまで変更 ----

            # 「TRACE」シナリオ
            else:
                message_file="trace_message.txt"
                print("Neither ERROR nor DOWN exist!")
                print("Interface status is normal, but there is an error in the communication path.")
                prediction_device_list = list(izawa_cunfusion_matrix.topk_excluding_ties(trace_df["Total"],k))

            #print("error_devices",error_device_list)
            print("prediction_devices",prediction_device_list)

            print("\nWhere errors can exist in the network model")
            # ファイルを読み取り専用モードで開く
            with open(message_file, 'r', encoding='utf-8') as file:
                content = file.read()  # ファイル全体を読み取る
                print(content)         # 内容を表示


            a = len(prediction_device_list)
            for prediction_device in prediction_device_list:
                if prediction_device in error_device_list:
                    confusion_matrix["TP"] += 1
                else:
                    confusion_matrix["FP"] += 1

            for error_device in error_device_list:
                if not error_device in prediction_device_list:
                    a += 1
                    confusion_matrix["FN"] += 1

            confusion_matrix["TN"] += 9 - a

        AUC_data[k] = confusion_matrix
        print(confusion_matrix)
        #izawa_cunfusion_matrix.calculate_metrics(confusion_matrix)

    print(AUC_data)