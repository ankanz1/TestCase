# Final ECG-QML Experiment Summary

## Executive summary

This report consolidates existing project results only. No model was retrained, no model artifact was changed, and no new experiment was run.

The current system is a research demonstration, not a clinical diagnostic system. The experiments do not demonstrate quantum advantage: the frozen QML model is substantially below the classical baselines in the reported comparisons.

## 1. Project pipeline

```text
ECG heartbeat: 187 signal values
        |
        v
Fitted PCA: 187 -> 8 features
        |
        v
8 qubits, 4-layer VQC / hybrid QML model
        |
        v
5-class heartbeat prediction: 0, 1, 2, 3, 4
        |
        v
Permutation-importance XAI
        |
        v
Offline Streamlit demonstration frontend
```

Class terminology used by the project:

- `0 = N`: Normal beat
- `1 = S`: Supraventricular ectopic beat
- `2 = V`: Ventricular ectopic beat
- `3 = F`: Fusion beat
- `4 = Q`: Unknown beat

## 2. Classical model results

The project benchmark figures requested for this consolidated summary are:

| Model | Reported Macro-F1 |
|---|---:|
| MLP, 187 features | **81.09%** |
| Full-feature XGBoost, 187 features | **85.86%** |
| PCA-8 XGBoost | **59.56%** |

### Metric provenance note

The existing saved artifacts do not all preserve the same split/evaluation record:

- `outputs/xgboost_metrics.json` contains full-feature XGBoost untouched-test Macro-F1 `0.8585565933`, which rounds to **85.86%**.
- `outputs/xgb_pca8_metrics.json` contains PCA-8 XGBoost validation Macro-F1 `0.5945560533`, which rounds to **59.46%**. The project benchmark figure requested above is **59.56%**; no new PCA-8 test evaluation was run to reconcile that difference.
- `outputs/results.json` contains MLP validation metrics, including Macro-F1 `0.8353939157`; a separate saved MLP untouched-test Macro-F1 of **81.09%** is not present in the current JSON artifacts.

These differences are reported explicitly to avoid implying that a missing test evaluation was regenerated.

## 3. Final QML configuration and untouched-test result

The selected frozen QML configuration is:

- Qubits: **8**
- VQC depth: **4 layers**
- Trainable parameters: **141**
- Training mode: **balanced**
- PCA: **187 -> 8 features**
- Final untouched-test samples: **21,892**

Saved final untouched-test results from `outputs/qml_balanced_test_metrics.json`:

| Metric | Result |
|---|---:|
| Accuracy | **56.687%** |
| Balanced accuracy | **59.626%** |
| Macro-F1 | **35.184%** |

The underlying saved values are accuracy `0.5668737438`, balanced accuracy `0.5962587632`, and Macro-F1 `0.3518437223`.

## 4. VQC depth scan

The depth scan used validation Macro-F1 as the selection criterion:

| VQC depth | Best validation Macro-F1 |
|---:|---:|
| 2 layers | **31.41%** |
| 4 layers | **35.75%** |
| 6 layers | **33.10%** |
| 8 layers | **33.42%** |

Depth 4 was selected because it achieved the highest saved validation Macro-F1: `0.3574814574`. Depth 6 and depth 8 did not improve Macro-F1, despite depth 8 having higher validation balanced accuracy than depth 4. The selection criterion was Macro-F1, so the 4-layer configuration was retained.

## 5. Controlled comparisons

### Full-feature XGBoost versus PCA-8 XGBoost

The full-feature XGBoost benchmark is **85.86% Macro-F1**, while the PCA-8 XGBoost benchmark is **59.56% Macro-F1** as recorded for this summary. This large reduction indicates that compressing 187 ECG values into 8 PCA coordinates removes information that the classical tree model uses for heartbeat discrimination. The exact saved PCA-8 artifact is validation-only and reports `59.4556%`, so the split difference must be kept in mind.

### PCA-8 XGBoost versus QML

Using the requested project benchmark values, PCA-8 XGBoost reaches **59.56% Macro-F1**, compared with **35.184%** for the frozen QML model. The gap is approximately **24.38 percentage points** in favor of PCA-8 XGBoost. Both models operate on an 8-feature PCA representation, so this comparison indicates that the current QML model does not outperform a classical model under the same compressed-feature setting.

The saved PCA-8 XGBoost result is validation-only, whereas the QML result is the final untouched-test evaluation; therefore this is evidence of a performance gap in the available experiment records, not a perfectly matched final-test comparison.

## 6. QML training evidence

The saved balanced QML training artifact reports:

- `quantum_grad_is_none = False`
- `quantum_parameter_gradient_norm = 0.06177539`
- `quantum_weight_change_norm = 0.00938073`

This confirms that the quantum parameters received a non-null gradient and changed during the recorded training run. It demonstrates functioning gradient flow and parameter updates; it does not demonstrate quantum advantage or superior predictive performance.

## 7. XAI implementation

The implemented XAI component explains one frozen QML prediction as follows:

1. Accepts one ECG heartbeat with exactly 187 values.
2. Reuses the existing fitted standard scaler and PCA artifact to produce 8 PCA features.
3. Reuses the frozen balanced QML model and its probability-like softmax output.
4. Records the baseline predicted-class probability.
5. Replaces one PCA coordinate at a time with the PCA-centered reference value, zero.
6. Recomputes the predicted-class probability and measures the absolute score change.
7. Ranks all 8 PCA features by this importance score.
8. Projects the ranked PCA importance back toward the original 187 ECG positions using the absolute PCA component loadings.
9. Produces a visualization containing the waveform and the loading-weighted importance overlay.

This is model interpretability, not clinical diagnosis. Highlighted waveform regions indicate model sensitivity under this perturbation method; they are not medically causal regions.

## 8. Streamlit frontend

The current offline Streamlit frontend in `app.py` provides:

- selection of a sample from `data/mitbih_test.csv`;
- CSV/TXT upload;
- manual entry of 187 ECG values;
- validation of count, numeric conversion, and finite values;
- frozen QML prediction using the balanced model configuration;
- probability-score display from the model's softmax output;
- 187-point ECG waveform visualization;
- XAI importance visualization over the waveform;
- display of the top 3 important PCA features;
- cached test-data and explanation loading so the model path is not retrained or repeatedly reloaded during normal interaction.

The frontend is intended for local, offline demonstration using the existing model and data files.

## 9. Limitations and interpretation

- The current QML model does not outperform the classical baselines.
- PCA compression from 187 to 8 features causes substantial information loss, as shown by the drop from full-feature XGBoost to PCA-8 XGBoost.
- The dataset is heartbeat-level. It is not a direct patient-level disease diagnosis dataset.
- A model class or probability score must not be presented as a clinical diagnosis, confirmed disease, or patient-specific medical conclusion.
- The highlighted XAI regions must not be described as medically causal.
- The current experiments do not demonstrate quantum advantage.
- The available saved artifacts do not provide perfectly matched untouched-test metrics for every classical model; split labels must be preserved when comparing results.

## Existing source artifacts

- QML final untouched test: `outputs/qml_balanced_test_metrics.json`
- QML validation and training evidence: `outputs/qml_balanced_metrics.json`
- QML depth scan: `outputs/qml_depth_scan/depth_scan_summary.json`
- Full-feature XGBoost test: `outputs/xgboost_metrics.json`
- PCA-8 XGBoost validation: `outputs/xgb_pca8_metrics.json`
- MLP validation artifact: `outputs/results.json`
- XAI implementation: `src/explain_qml.py`
- Streamlit frontend: `app.py`
