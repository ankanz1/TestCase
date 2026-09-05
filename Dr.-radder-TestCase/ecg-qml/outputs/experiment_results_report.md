# Consolidated Experiment Results

## Scope

This report consolidates only the saved experiment artifacts in `outputs/` plus the newly completed untouched-test evaluation supplied for the frozen QML model. No model was retrained and no model artifact was modified.

The dataset has 187 input features. The PCA-based experiments use 8 PCA components. The QML configuration is frozen at 8 qubits and 4 variational-circuit layers.

## Metric definitions and split policy

- **Validation** means the saved validation split used during model development or depth selection.
- **Final untouched test** means evaluation on the held-out test set with 21,892 samples. These values are reported only where a saved artifact exists or where the newly completed QML evaluation was supplied.
- The MLP artifact names its macro-averaged precision and recall fields `precision` and `recall`; they are reported below as macro precision and macro recall because the training code computes them with `average="macro"`.
- A missing final-test value is reported as **not available**, not inferred from validation.

## Model results

### Validation metrics

| Model | Features | Accuracy | Balanced accuracy | Macro precision | Macro recall | Macro F1 | Weighted F1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| MLP | 187 | 0.964993 | 0.798264 | 0.882314 | 0.798264 | 0.835394 | 0.963660 |
| Full-feature XGBoost | 187 | not available | not available | not available | not available | not available | not available |
| PCA-8 XGBoost | 8 | 0.819000 | 0.806672 | 0.538248 | 0.806672 | 0.594556 | 0.853475 |
| QML, 8 qubits, 4 layers | 8 | 0.562500 | 0.570714 | 0.356285 | 0.570714 | 0.357481 | 0.646030 |

The full-feature XGBoost output was subsequently overwritten by its test evaluation, so its earlier validation metrics are not present in the existing saved artifacts.

### Final untouched-test metrics

| Model | Test samples | Accuracy | Balanced accuracy | Macro precision | Macro recall | Macro F1 | Weighted F1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| MLP | not available | not available | not available | not available | not available | not available | not available |
| Full-feature XGBoost | 21,892 | 0.967111 | 0.908692 | 0.821171 | 0.908692 | 0.858557 | 0.968613 |
| PCA-8 XGBoost | not available | not available | not available | not available | not available | not available | not available |
| QML, 8 qubits, 4 layers | 21,892 | 0.566874 | 0.596259 | 0.350283 | 0.596259 | 0.351844 | 0.648690 |

The QML test values are the newly completed evaluation of the frozen 8-qubit, 4-layer model:

- Accuracy: 0.5668737438333638
- Balanced accuracy: 0.5962587632313106
- Macro precision: 0.35028257299355126
- Macro recall: 0.5962587632313106
- Macro F1: 0.351843722284212
- Weighted F1: 0.6486902214362236

## QML depth scan

All depth-scan rows use 8 qubits, 5,000 training samples, and 2,000 validation samples. Values below are the saved best-validation results for each depth.

| VQC depth | Trainable parameters | Best validation Macro F1 | Validation balanced accuracy | Validation accuracy |
|---:|---:|---:|---:|---:|
| 2 layers | 93 | 0.314125 | 0.545717 | 0.483000 |
| 4 layers | 141 | 0.357481 | 0.570714 | 0.562500 |
| 6 layers | 189 | 0.331046 | 0.558395 | 0.501500 |
| 8 layers | 237 | 0.334204 | 0.582041 | 0.517500 |

### Selected depth

The selected depth is **4 layers**. It achieved the highest saved validation Macro F1, 0.3574814574, compared with 0.3141245806 at depth 2, 0.3310463384 at depth 6, and 0.3342043218 at depth 8. The 8-layer model had higher validation balanced accuracy than the 4-layer model, but its Macro F1 and accuracy were lower. Macro F1 was the selection criterion, so the 4-layer model was retained.

## PCA-8 XGBoost versus QML

### Validation comparison

On the saved validation split, PCA-8 XGBoost outperformed the selected QML model on every reported aggregate metric:

- Accuracy: 0.819000 versus 0.562500, a difference of 0.256500.
- Balanced accuracy: 0.806672 versus 0.570714, a difference of 0.235958.
- Macro precision: 0.538248 versus 0.356285, a difference of 0.181963.
- Macro recall: 0.806672 versus 0.570714, a difference of 0.235958.
- Macro F1: 0.594556 versus 0.357481, a difference of 0.237075.
- Weighted F1: 0.853475 versus 0.646030, a difference of 0.207446.

The QML untouched-test result is also substantially below the full-feature XGBoost untouched-test result: Macro F1 is 0.351844 versus 0.858557, and balanced accuracy is 0.596259 versus 0.908692. A final-test comparison between PCA-8 XGBoost and QML cannot be completed from the existing artifacts because no PCA-8 XGBoost untouched-test metrics are saved.

## Conclusion

The saved experiments do not demonstrate quantum advantage. The selected PCA-8 QML model reaches 0.351844 Macro F1 and 0.596259 balanced accuracy on the untouched test set, while full-feature XGBoost reaches 0.858557 Macro F1 and 0.908692 balanced accuracy on that same test set. On validation, PCA-8 XGBoost also exceeds QML by 0.237075 Macro F1 points. These results support QML as an experimental hybrid baseline in this setup, not as evidence of an accuracy or balanced-performance advantage over classical models.

The conclusion is limited to these experiments, saved splits, preprocessing pipeline, simulator/model configuration, and reported metrics. It does not establish that quantum methods can never provide an advantage under other data, feature mappings, circuit designs, training procedures, hardware, or evaluation protocols.

## Source artifacts

- MLP validation: `outputs/results.json`
- Full-feature XGBoost untouched test: `outputs/xgboost_metrics.json`
- PCA-8 XGBoost validation: `outputs/xgb_pca8_metrics.json`
- QML 8-qubit, 4-layer validation: `outputs/qml_balanced_metrics.json`
- QML untouched test: `outputs/qml_balanced_test_metrics.json`
- QML depth scan: `outputs/qml_depth_scan/depth_*_layers_metrics.json` and `outputs/qml_depth_scan/depth_scan_summary.json`
