import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


def topk_excluding_ties(series: pd.Series, k: int) -> pd.Index:
    """
    series を値の降順でソートし、
    - k番目の値 == (k+1)番目の値 ならば、
        その同値を持つ要素をすべて除外して返す
    - そうでなければ、
        上位 k 件を返す
    結果として得られるのは "Index" (行名)。

    例:
      Cf1=10, Cf2=9, Cf3=8, Cf4=8, Cf5=8 のとき k=3:
        通常だと Cf1, Cf2, Cf3 (10, 9, 8) を取るが
        3番目(8) と 4番目(8) が同値なので 8 をすべて除外し、
        最終的に Cf1, Cf2 だけ返す。
    """

    s_sorted = series.sort_values(ascending=False)

    # len(s_sorted) が k 未満なら、存在する要素すべてが「上位k」
    if len(s_sorted) < k:
        return s_sorted.index

    # k番目まではインデックスで k-1
    kth_value = s_sorted.iloc[k-1]

    # k+1 番目と比較するには、要素数が k を超える必要がある
    # (k個ピッタリしかなければそもそも k+1 番目は存在しない)
    if len(s_sorted) > k:
        kplus1_value = s_sorted.iloc[k]
        # k番目と (k+1)番目が同値であれば、その値を持つ要素は全除外
        if kth_value == kplus1_value:
            # kth_value より大きい値だけ残す (strictly greater)
            s_sorted = s_sorted[s_sorted > kth_value]
            return s_sorted.index

    # 同値ではなかった場合 → 上位kのインデックスを返す
    return s_sorted.iloc[:k].index

def create_confusion_matrix_labels_topk(final_df: pd.DataFrame, k: int = 1) -> pd.DataFrame:
    """
    final_df (行: Cf1.., 列: Cf1.. など) に対し
    各列(実際の機器)で上位k件を抽出 (k番目とk+1番目が同値なら除外)。
    さらに「正解機器が複数ある」ケースに対応し、
     - 行=予測機器
     - 列=実際(正解)の機器(複数)
    として各セルを "TP"/"FP"/"FN"/"TN" に分類する。
    """

    # 同じサイズで、全セルを "TN" で初期化
    confusion_labels = pd.DataFrame(
        "TN",
        index=final_df.index,
        columns=final_df.columns
    )

    print()

    # 各列(実際ラベル)について処理
    for col_label in final_df.columns:
        # この列に紐づく「正解機器」の集合 (例: ["Cf6","Cf3"])
        actual_set = col_label.split('_')

        # その列のSeriesを取得し、予測上位k (同値除外) を取り出す
        col_series = final_df[col_label]
        predicted_topk = topk_excluding_ties(col_series, k)
        predicted_set = set(predicted_topk)  # 予測された行ラベルの集合

        print(f"actual_set={actual_set}, predicted_topk={list(predicted_set)}")

        # 行ラベル(=device候補)それぞれに対して TP/FP/FN/TN を割り振る
        for device in final_df.index:
            if device in predicted_set:
                # 予測された
                if device in actual_set:
                    confusion_labels.loc[device, col_label] = "TP"
                else:
                    confusion_labels.loc[device, col_label] = "FP"
            else:
                # 予測されなかった
                if device in actual_set:
                    confusion_labels.loc[device, col_label] = "FN"
                else:
                    confusion_labels.loc[device, col_label] = "TN"

    return confusion_labels

def evaluate_confusion_matrix_label_df(label_df: pd.DataFrame):
    """
    label_df: 各セルが "TP" / "FP" / "FN" / "TN" の NxN 行列 (混同行列ラベル)
    から TP, FP, FN, TN の合計数を算出し、以下を計算して表示する:
      - 正解率 (Accuracy)
      - 精度 (Precision)
      - 再現率 (Recall)
      - 陰性的中率 (Negative Predictive Value)
      - 特異度 (Specificity)
    """
    # 各セルをフラットに並べる
    all_labels = label_df.values.flatten()

    # 合計カウントを計算
    TP = (all_labels == "TP").sum()
    FP = (all_labels == "FP").sum()
    FN = (all_labels == "FN").sum()
    TN = (all_labels == "TN").sum()
    total = TP + FP + FN + TN

    # 各指標を計算（0除算の可能性に注意）
    accuracy = (TP + TN) / total if total else 0.0
    precision = TP / (TP + FP) if (TP + FP) else 0.0
    recall = TP / (TP + FN) if (TP + FN) else 0.0
    npv = TN / (TN + FN) if (TN + FN) else 0.0  # Negative Predictive Value
    specificity = TN / (TN + FP) if (TN + FP) else 0.0

    # 結果を表示 (または返す)
    print("\n=== Confusion Matrix Summary ===")
    print(f"TP: {TP}, FP: {FP}, FN: {FN}, TN: {TN}")
    print(f"Accuracy:  {accuracy:.3f}")
    print(f"Precision: {precision:.3f}")
    print(f"Recall:    {recall:.3f}")
    print(f"NPV:       {npv:.3f}")
    print(f"Specificity: {specificity:.3f}")

def display_table_with_matplotlib(df, label_df, is_legend=True):
    """
    pandasのDataFrameをmatplotlibのtableとして描画する関数。
    第一引数: 表示するデータフレーム (df)。
    第二引数: 色付けの基準となる混同行列データフレーム (label_df)。
    TP (True Positive): 緑
    FP (False Positive): 赤
    FN (False Negative): 黄

    ※ 表のサイズは行数、列数に応じて自動調整する。
      カラム幅・行高は一定とし、表の外側余白は最小限に。
    """

    # ----------------------------------------------------------
    # 1) 図のサイズを行・列数に応じて動的に決定する
    #    例: カラムあたり 1.2 inch, 行あたり 0.4 inch など
    # ----------------------------------------------------------
    row_count = df.shape[0]
    col_count = df.shape[1]

    # ヘッダ (列ラベル) や行ラベル分のスペースを少し考慮
    # 数値はチューニングに応じて調整可能
    col_unit_width = 1.1  # カラム1つあたりの幅
    row_unit_height = 0.5  # 行1つあたりの高さ
    # （行数 + 1）は、テーブルの列ラベル分を考慮
    # （列数 + 1）は、テーブルの行ラベル分を考慮

    fig_width = (col_count + 1) * col_unit_width
    fig_height = (row_count + 1) * row_unit_height

    # 図を作成
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.axis('off')  # 軸は非表示

    # ----------------------------------------------------------
    # 2) テーブル内部に表示するテキストとヘッダを作成
    # ----------------------------------------------------------
    # 表示用のセルテキストをDataFrameから作成 (左端に行ラベルを表示)
    table_data = [[df.index[i]] + list(df.iloc[i]) for i in range(len(df))]
    col_labels = ["Pred/True"] + list(df.columns)

    # ----------------------------------------------------------
    # 3) label_df の値 (TP, FN, FP など) に応じたセルの背景色を付与
    # ----------------------------------------------------------
    cell_colors = []
    for i in range(len(df)):   # 行(データ部分)
        row_colors = []
        for j in range(len(df.columns)):  # 列(データ部分)
            if label_df.iloc[i, j] == "TP":
                row_colors.append("lightgreen")  # TP: 緑
            elif label_df.iloc[i, j] == "FN":
                row_colors.append("lightcoral")  # FN: 赤
            elif label_df.iloc[i, j] == "FP":
                row_colors.append("khaki")       # FP: 黄
            else:
                row_colors.append("white")       # その他: 白
        # 行ラベル列は白で統一するため、先頭に 'white' を入れる
        cell_colors.append(["white"] + row_colors)

    # ----------------------------------------------------------
    # 4) テーブルの作成
    # ----------------------------------------------------------
    table = ax.table(
        cellText=table_data,
        colLabels=col_labels,
        cellLoc="center",   # 文字を中心に配置
        loc="center",   # 軸の左上から配置(後で余白を調整する)
        cellColours=cell_colors,
        edges='closed',     # 罫線を閉じた形にしたい場合
    )

    # ----------------------------------------------------------
    # 5) テーブルのフォントサイズやセルサイズを統一する
    # ----------------------------------------------------------
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    # 各セルの幅・高さを一定にするための手法
    # cell.get_width() / cell.get_height() で計算しスケールするやり方もあるが
    # 手動で scale(幅スケール, 高さスケール) を設定
    table.scale(1, 1.5)
    # ↑ 引数は試行錯誤で調整してください (スケール前のセルサイズをどの程度にするか)

    # ----------------------------------------------------------
    # 6) 凡例 (オプション)
    # ----------------------------------------------------------
    if is_legend:
        # 凡例パッチ
        legend_elements = [
            Patch(facecolor="lightgreen", edgecolor="black", label="TP (True Positive)"),
            Patch(facecolor="khaki",     edgecolor="black", label="FP (False Negative)"),
            Patch(facecolor="lightcoral", edgecolor="black", label="FN (False Positive)"),
            Patch(facecolor="white",     edgecolor="black", label="TN (True Negative)"),
        ]
        # 凡例の配置: 下部に横並び
        #fig.legend(handles=legend_elements, loc="lower center", ncol=4)
        fig.legend(handles=legend_elements, loc="lower center", bbox_to_anchor=(0.5, 0.1), ncol=4)


    # ----------------------------------------------------------
    # 7) 余白を最小限に抑えてレイアウト
    # ----------------------------------------------------------
    # 方法1: tight_layout を使う
    # plt.tight_layout() だと凡例が被ることがあるため、rect= で微調整して使う
    plt.tight_layout(rect=[0, 0, 1, 1])

    # 方法2: subplots_adjust で余白を直接調整する場合
    # plt.subplots_adjust(
    #     left=0.01, right=0.99, top=0.95, bottom=0.05,
    #     wspace=0, hspace=0
    # )

    plt.show()


def calculate_metrics(confusion_matrix):
    # 各値の取得
    TP = confusion_matrix['TP']
    TN = confusion_matrix['TN']
    FP = confusion_matrix['FP']
    FN = confusion_matrix['FN']

    # 評価指標の計算
    # 正解率 (Accuracy)
    accuracy = (TP + TN) / (TP + TN + FP + FN)

    # 適合率 (Precision)
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0

    # 再現率 (Recall) / 感度 (Sensitivity)
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0

    # 特異度 (Specificity)
    specificity = TN / (TN + FP) if (TN + FP) > 0 else 0

    # F1スコア
    f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    # 偽陽性率 (False Positive Rate, FPR)
    fpr = FP / (FP + TN) if (FP + TN) > 0 else 0

    # 偽陰性率 (False Negative Rate, FNR)
    fnr = FN / (FN + TP) if (FN + TP) > 0 else 0

    # Matthews相関係数 (MCC)
    mcc_numerator = (TP * TN) - (FP * FN)
    mcc_denominator = ((TP + FP) * (TP + FN) * (TN + FP) * (TN + FN)) ** 0.5
    mcc = mcc_numerator / mcc_denominator if mcc_denominator > 0 else 0

    # 結果の出力
    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("Specificity:", specificity)
    print("F1 Score:", f1_score)
    print("False Positive Rate (FPR):", fpr)
    print("False Negative Rate (FNR):", fnr)
    print("Matthews Correlation Coefficient (MCC):", mcc)