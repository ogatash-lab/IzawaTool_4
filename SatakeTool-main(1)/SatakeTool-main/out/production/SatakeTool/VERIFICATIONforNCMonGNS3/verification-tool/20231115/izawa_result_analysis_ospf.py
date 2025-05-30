import yaml
import pandas as pd
import os
import glob
import re
import copy

import izawa_cunfusion_matrix

# YAMLファイルのパスを指定
ideal_file_path = "../izawa_result/cmd_kiki_temp.yaml"
#ideal_file_path = "../izawa_result/cmd_kiki_cost_temp.yaml"

verification_file_path = "result_table_id"  # ディレクトリ例
#verification_file_path = "result_table_id_2-6"  # ディレクトリ例

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


if __name__ == "__main__":

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

    # ディレクトリ内の全ファイルで集計した最終的な「Total」列のみを保持する DataFrame を用意
    # 行ラベルは Cf1~Cf9 で固定し、列はあとでファイルごとに追加していく
    row_labels = ["Cf1","Cf2","Cf3","Cf4","Cf5","Cf6","Cf7","Cf8","Cf9"]
    final_DOWN_total_df = pd.DataFrame(index=row_labels)
    final_MISS_total_df = pd.DataFrame(index=row_labels)

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

        for top_key in ideal_data.keys():
            neighbor_relationship = copy.deepcopy(neighbor_devices)

            if "-" in top_key:
                device1, device2 = top_key.split("-")
                print("device1",device1)
                print("device2",device2)

                # device1のリストからdevice2を削除
                if device2 in neighbor_relationship.get(device1, []):
                    neighbor_relationship[device1].remove(device2)

                # device2のリストからdevice1を削除
                if device1 in neighbor_relationship.get(device2, []):
                    neighbor_relationship[device2].remove(device1)
            print(neighbor_relationship)


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

        # 各ファイルごとの DOWN, MISS を DataFrame 化して表示
        print("\n[DOWN result for this file]")
        down_df = dict_to_dataframe(DOWN_result_table)
        print(down_df)

        print("\n[MISS result for this file]")
        miss_df = dict_to_dataframe(MISS_result_table)
        print(miss_df)

        # 各ファイルごとに計算したダウン/ミスの「Total」列だけをまとめて保存
        # 列ラベルは device_label (例: "Cf6_Cf3") とする
        final_DOWN_total_df[device_label] = down_df["Total"]
        final_MISS_total_df[device_label] = miss_df["Total"]

    # 全ファイル処理後、「[FINAL DOWN TOTAL]」「[FINAL MISS TOTAL]」として表示
    print("\n===== [FINAL DOWN TOTAL] =====")
    print(final_DOWN_total_df)

    print("\n===== [FINAL MISS TOTAL] =====")
    print(final_MISS_total_df)

    # 8) confusion matrix (ユーザー定義関数)
    final_DOWN_df_labels = izawa_cunfusion_matrix.create_confusion_matrix_labels_topk(final_DOWN_total_df, k=1)
    final_MISS_df_labels = izawa_cunfusion_matrix.create_confusion_matrix_labels_topk(final_MISS_total_df, k=1)

    izawa_cunfusion_matrix.evaluate_confusion_matrix_label_df(final_DOWN_df_labels)
    izawa_cunfusion_matrix.evaluate_confusion_matrix_label_df(final_MISS_df_labels)
    # 9) 追加: final_df を matplotlib で表として可視化
    izawa_cunfusion_matrix.display_table_with_matplotlib(final_DOWN_total_df, final_DOWN_df_labels)
    izawa_cunfusion_matrix.display_table_with_matplotlib(final_MISS_total_df, final_MISS_df_labels)
