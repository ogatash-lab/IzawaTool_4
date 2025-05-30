import matplotlib.pyplot as plt
from sklearn.metrics import auc

# 与えられたデータ (閾値: confusion matrixの結果)
#data = {0: {'TP': 0, 'TN': 56, 'FP': 0, 'FN': 16}, 1: {'TP': 4, 'TN': 52, 'FP': 4, 'FN': 12}, 2: {'TP': 11, 'TN': 51, 'FP': 5, 'FN': 5}, 3: {'TP': 13, 'TN': 45, 'FP': 11, 'FN': 3}, 4: {'TP': 15, 'TN': 40, 'FP': 16, 'FN': 1}, 5: {'TP': 15, 'TN': 31, 'FP': 25, 'FN': 1}, 6: {'TP': 15, 'TN': 23, 'FP': 33, 'FN': 1}, 7: {'TP': 15, 'TN': 16, 'FP': 40, 'FN': 1}, 8: {'TP': 15, 'TN': 7, 'FP': 49, 'FN': 1}, 9: {'TP': 16, 'TN': 0, 'FP': 56, 'FN': 0}}
data = {0: {'TP': 0, 'TN': 56, 'FP': 0, 'FN': 16}, 1: {'TP': 5, 'TN': 54, 'FP': 2, 'FN': 11}, 2: {'TP': 9, 'TN': 49, 'FP': 7, 'FN': 7}, 3: {'TP': 12, 'TN': 44, 'FP': 12, 'FN': 4}, 4: {'TP': 12, 'TN': 37, 'FP': 19, 'FN': 4}, 5: {'TP': 14, 'TN': 30, 'FP': 26, 'FN': 2}, 6: {'TP': 15, 'TN': 23, 'FP': 33, 'FN': 1}, 7: {'TP': 15, 'TN': 16, 'FP': 40, 'FN': 1}, 8: {'TP': 15, 'TN': 7, 'FP': 49, 'FN': 1}, 9: {'TP': 16, 'TN': 0, 'FP': 56, 'FN': 0}}

# 1) 閾値をソート
thresholds = sorted(data.keys())

# 2) ROC用 (TPR, FPR) と F-measure 用のリストを用意
tpr_list = []
fpr_list = []
fmeasure_list = []

for th in thresholds:
    TP = data[th]['TP']
    TN = data[th]['TN']
    FP = data[th]['FP']
    FN = data[th]['FN']

    # --- ROC 用計算 ---
    # TPR = TP / (TP + FN)
    if (TP + FN) != 0:
        tpr = TP / (TP + FN)
    else:
        tpr = 0

    # FPR = FP / (FP + TN)
    if (FP + TN) != 0:
        fpr = FP / (FP + TN)
    else:
        fpr = 0

    tpr_list.append(tpr)
    fpr_list.append(fpr)

    # --- F-measure 用計算 ---
    # Precision = TP / (TP + FP)
    if (TP + FP) != 0:
        precision = TP / (TP + FP)
    else:
        precision = 0

    # Recall = TPR
    recall = tpr

    # F-measure (F1スコア) = 2 * (P * R) / (P + R)
    if (precision + recall) != 0:
        fmeasure = 2 * precision * recall / (precision + recall)
    else:
        fmeasure = 0

    fmeasure_list.append(fmeasure)

# 3) ROC AUC の計算
# FPR(横軸)でソート → TPR と合わせて auc() で面積を算出
roc_points = list(zip(thresholds, fpr_list, tpr_list))
# (threshold, FPR, TPR) のタプルを、FPR でソート
roc_points_sorted = sorted(roc_points, key=lambda x: x[1])
sorted_thresholds_roc = [p[0] for p in roc_points_sorted]
sorted_fpr = [p[1] for p in roc_points_sorted]
sorted_tpr = [p[2] for p in roc_points_sorted]
roc_auc = auc(sorted_fpr, sorted_tpr)

# 結果の表示
print("閾値:", thresholds)
print("FPR:", fpr_list)
print("TPR:", tpr_list)
print("F-measure:", fmeasure_list)
print(f"ROC AUC: {roc_auc:.3f}")

# グラフ描画
plt.figure(figsize=(12, 6))

# --- (1) ROC曲線のプロット ---
plt.subplot(1, 2, 1)
plt.plot(sorted_fpr, sorted_tpr, marker='o', label=f"ROC curve (AUC = {roc_auc:.3f})")
plt.plot([0, 1], [0, 1], linestyle='--', color='gray')
plt.title('ROC Curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend()
plt.grid(True)

# 各点の近くに閾値を文字で表示 (ROC)
for th, x, y in zip(sorted_thresholds_roc, sorted_fpr, sorted_tpr):
    plt.text(x, y, "top" + str(th), fontsize=9, ha='left', va='bottom')

# --- (2) F-measureのプロット ---
plt.subplot(1, 2, 2)
plt.plot(thresholds, fmeasure_list, marker='o', label='F-measure')
plt.title('F-measure vs Top K devices')
plt.xlabel('Top K devices')
plt.ylabel('F-measure (F1 Score)')
plt.ylim([0, 1.05])
plt.legend()
plt.grid(True)

# 各点の近くに閾値を文字で表示 (F-measure)
for x, y in zip(thresholds, fmeasure_list):
    plt.text(x, y, "top" + str(x), fontsize=9, ha='left', va='bottom')

plt.tight_layout()
plt.show()
