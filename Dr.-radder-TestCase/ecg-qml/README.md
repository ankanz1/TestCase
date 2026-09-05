# ECG Baseline Classifier

This project implements a classical PyTorch MLP baseline for ECG heartbeat classification using the MIT-BIH arrhythmia dataset.

## Structure

- `data/`: ECG CSVs
- `models/`: trained model, scaler, and metadata
- `src/`: training, evaluation, and prediction logic
- `scripts/`: sample test script
- `outputs/`: plots and evaluation results

## Quick start

From the project root:

```bash
python -m src.train
python scripts/test_model.py
```

The prediction interface is exposed as `src.predict.predict_ecg(ecg_values)` and accepts exactly 187 numeric ECG values.

## Dr. Radar UI integration

The frozen QML model is exposed locally through `api.py`:

```bash
python -m uvicorn api:app --host 127.0.0.1 --port 8000
```

- `GET /health` verifies that the balanced QML model and preprocessing artifacts load.
- `POST /predict/ecg` accepts `{ "ecg": [187 numeric values] }` and returns the class, softmax probability map, PCA feature importance, waveform, and 187-position XAI importance.

Start the existing Dr. Radar frontend separately from `Dr.-Radar-Uii/` with `npm install` followed by `npm run dev`. Its existing Express server proxies `/api/predict/ecg` to `ECG_QML_API_URL` or `http://127.0.0.1:8000` by default. Required local artifacts remain under `models/`; the API never retrains them.
