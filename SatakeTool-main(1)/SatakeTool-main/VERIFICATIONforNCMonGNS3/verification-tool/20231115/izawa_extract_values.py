
aaa = {0: {'TP': 0, 'TN': 56, 'FP': 0, 'FN': 16}, 1: {'TP': 5, 'TN': 54, 'FP': 2, 'FN': 11}, 2: {'TP': 9, 'TN': 49, 'FP': 7, 'FN': 7}, 3: {'TP': 12, 'TN': 44, 'FP': 12, 'FN': 4}, 4: {'TP': 12, 'TN': 37, 'FP': 19, 'FN': 4}, 5: {'TP': 14, 'TN': 30, 'FP': 26, 'FN': 2}, 6: {'TP': 15, 'TN': 23, 'FP': 33, 'FN': 1}, 7: {'TP': 15, 'TN': 16, 'FP': 40, 'FN': 1}, 8: {'TP': 15, 'TN': 7, 'FP': 49, 'FN': 1}, 9: {'TP': 16, 'TN': 0, 'FP': 56, 'FN': 0}}

confusion_matrix = aaa[2]


# Extract values from confusion matrix
TP = confusion_matrix['TP']
TN = confusion_matrix['TN']
FP = confusion_matrix['FP']
FN = confusion_matrix['FN']

# Calculate evaluation metrics
accuracy = (TP + TN) / (TP + TN + FP + FN)
precision = TP / (TP + FP) if (TP + FP) != 0 else 0
recall = TP / (TP + FN) if (TP + FN) != 0 else 0
npv = TN / (TN + FN) if (TN + FN) != 0 else 0
specificity = TN / (TN + FP) if (TN + FP) != 0 else 0
f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) != 0 else 0

# Display the results
print("Evaluation Metrics for the Confusion Matrix:")
print(f"Accuracy: {accuracy:.2f}")
print(f"Precision (Positive Predictive Value): {precision:.2f}")
print(f"Recall (Sensitivity): {recall:.2f}")
print(f"Negative Predictive Value (NPV): {npv:.2f}")
print(f"Specificity: {specificity:.2f}")
print(f"F1 Score: {f1_score:.2f}")