import matplotlib.pyplot as plt
from sklearn.metrics import auc

# 与えられたデータ (閾値: confusion matrixの結果)
data = {
    0: {'TP': 0,  'TN': 272, 'FP': 0,   'FN': 34},
    1: {'TP': 32, 'TN': 271, 'FP': 1,   'FN': 2},
    2: {'TP': 33, 'TN': 246, 'FP': 26,  'FN': 1},
    3: {'TP': 34, 'TN': 226, 'FP': 46,  'FN': 0},
    4: {'TP': 34, 'TN': 207, 'FP': 65,  'FN': 0},
    5: {'TP': 34, 'TN': 189, 'FP': 83,  'FN': 0},
    6: {'TP': 34, 'TN': 165, 'FP': 107, 'FN': 0},
    7: {'TP': 34, 'TN': 153, 'FP': 119, 'FN': 0},
    8: {'TP': 34, 'TN': 136, 'FP': 136, 'FN': 0},
    9: {'TP': 34, 'TN': 0,   'FP': 272, 'FN': 0}
}

# 1) まずは閾値をソートしておく(小さい順に並べる)
thresholds = sorted(data.keys())

# 2) ROC用 (TPR, FPR) を計算
tpr_list = []
fpr_list = []

# 3) PR曲線用 (Precision, Recall) を計算
precision_list = []
recall_list = []

for th in thresholds:
    TP = data[th]['TP']
    TN = data[th]['TN']
    FP = data[th]['FP']
    FN = data[th]['FN']

    # --- ROC 用計算 ---
    # TPR (True Positive Rate) = TP / (TP + FN)
    if (TP + FN) != 0:
        tpr = TP / (TP + FN)
    else:
        tpr = 0

    # FPR (False Positive Rate) = FP / (FP + TN)
    if (FP + TN) != 0:
        fpr = FP / (FP + TN)
    else:
        fpr = 0

    tpr_list.append(tpr)
    fpr_list.append(fpr)

    # --- PR 用計算 ---
    # Precision = TP / (TP + FP)
    if (TP + FP) != 0:
        precision = TP / (TP + FP)
    else:
        # 分母が 0 の場合は適切な扱いを決める必要がある
        # ここでは 0 としておく
        precision = 0

    # Recall = TPR = TP / (TP + FN)
    # (すでに tpr に入っているので使い回し)
    recall = tpr

    precision_list.append(precision)
    recall_list.append(recall)

# 4) AUC の計算 (ROC)
# ROC曲線は FPR(横軸)でソートして TPR を並べ替え、その面積を auc() で計算
sorted_pairs_roc = sorted(zip(fpr_list, tpr_list), key=lambda x: x[0])
sorted_fpr = [p[0] for p in sorted_pairs_roc]
sorted_tpr = [p[1] for p in sorted_pairs_roc]
roc_auc = auc(sorted_fpr, sorted_tpr)

# 5) AUPRC の計算 (PR)
# PR曲線は Recall(横軸)でソートして Precision を並べ替え、その面積を auc() で計算
sorted_pairs_pr = sorted(zip(recall_list, precision_list), key=lambda x: x[0])
sorted_recall = [p[0] for p in sorted_pairs_pr]
sorted_precision = [p[1] for p in sorted_pairs_pr]
pr_auc = auc(sorted_recall, sorted_precision)

print("閾値:", thresholds)
print("FPR:", fpr_list)
print("TPR:", tpr_list)
print("Precision:", precision_list)
print("Recall:", recall_list)
print(f"ROC AUC: {roc_auc:.3f}")
print(f"PR AUC (Average Precision): {pr_auc:.3f}")

# ROC曲線のプロット
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(sorted_fpr, sorted_tpr, marker='o', label=f"ROC curve (AUC = {roc_auc:.3f})")
plt.plot([0, 1], [0, 1], linestyle='--', color='gray')
plt.title('ROC Curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend()
plt.grid(True)

# PR曲線のプロット
plt.subplot(1, 2, 2)
plt.plot(sorted_recall, sorted_precision, marker='o', label=f"PR curve (AUC = {pr_auc:.3f})")
# 適宜、0~1のガイドライン等を追加
plt.title('Precision-Recall Curve')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.ylim([0, 1.05])
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
