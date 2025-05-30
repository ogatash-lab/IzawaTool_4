import yaml
import pandas as pd
import os
import glob
import re

import izawa_cunfusion_matrix

# YAMLファイルのパスを指定
#2-6結線
#ideal_file_path = "../izawa_result/cmd_kiki_cost_temp.yaml"

ideal_file_path = "../izawa_result/cmd_kiki_temp.yaml"
verification_file_path = "result_table_cost"  # ディレクトリ例

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
    df["Total"] = df.sum(axis=1)  # 各行の値を合計する列を追加
    return df


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
    # 1) ideal_file_path (単一ファイル) をロード
    ideal_data = load_yaml(ideal_file_path)

    # 2) verification_file_path がディレクトリかファイルかを判定
    if os.path.isdir(verification_file_path):
        # ディレクトリ内の .yaml ファイルをすべて取得
        yaml_files = glob.glob(os.path.join(verification_file_path, "*.yaml"))
    else:
        # 1つのファイルのみをリスト化
        yaml_files = [verification_file_path]

    # 3) フォルダ内すべてのファイルで処理した「Total」列を集約するためのDataFrameを用意
    row_labels = ["Cf1","Cf2","Cf3","Cf4","Cf5","Cf6","Cf7","Cf8","Cf9"]
    final_df = pd.DataFrame(index=row_labels)

    # 4) ファイルごとに処理
    for vf_path in yaml_files:
        print("\n===== Verification file: {} =====".format(vf_path))
        verification_data = load_yaml(vf_path)

        # ファイル名から何らかのデバイス名を抽出する場合 (任意)
        pattern = r"(Cf\d+)"
        devices = re.findall(pattern, vf_path)
        if devices:
            col_label = "_".join(devices)   # 例: ["Cf8","Cf3"] → "Cf8_Cf3"
        else:
            col_label = os.path.splitext(os.path.basename(vf_path))[0]

        # ideal_data の top_key (例: cost の中に { 'none': {...}, 'hoge': {...}, ... } ) を全部見る
        result_table_for_this_file = {}
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
            result_table_for_this_file[top_key] = list(trace_table.values())

        # 5) ファイルごとの結果をDataFrame化
        df_for_this_file = dict_to_dataframe(result_table_for_this_file)
        print(df_for_this_file)  # 中間確認: 各行 Cf1..Cf9, 各列 top_key, "Total" 列あり

        # 6) 「Total」列だけを最終集約用データフレームに追加
        final_df[col_label] = df_for_this_file["Total"]

    # 7) 全ファイル処理後、集約した「Total」列だけの最終結果を出力
    print("\n===== [FINAL TOTAL for All Files] =====")
    print(final_df)

    # 8) confusion matrix (ユーザー定義関数)
    df_labels = izawa_cunfusion_matrix.create_confusion_matrix_labels_topk(final_df, k=1)
    print("\n===== [Confusion matrix] =====")
    print(df_labels)
    izawa_cunfusion_matrix.evaluate_confusion_matrix_label_df(df_labels)

    print("\n===== [FINAL TOTAL for All Files] =====")
    print(final_df)

    # 9) 追加: final_df を matplotlib で表として可視化
    izawa_cunfusion_matrix.display_table_with_matplotlib(final_df, df_labels, True)
