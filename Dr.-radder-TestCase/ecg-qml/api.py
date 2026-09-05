from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.explain_qml import _load_frozen_qml_artifacts, explain_ecg


class EcgRequest(BaseModel):
    ecg: list[float] = Field(..., min_length=187, max_length=187)


app = FastAPI(title="ECG-QML Inference API", version="1.0.0")


def _build_response(explanation: dict[str, Any]) -> dict[str, Any]:
    prediction = explanation["prediction"]
    return {
        "predicted_class": prediction["class_id"],
        "class_name": prediction["class_name"],
        "score": prediction["score"],
        "probabilities": prediction["probabilities"],
        "top_pca_features": explanation["ranked_pca_features"][:3],
        "explanation": {
            "notice": explanation["interpretability_notice"],
            "method": explanation["permutation_method"],
        },
        "waveform": explanation["waveform"],
        "importance": explanation["original_position_importance"],
    }


@app.get("/health")
def health() -> dict[str, str]:
    try:
        _load_frozen_qml_artifacts("balanced")
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Frozen QML artifacts unavailable: {exc}") from exc
    return {"status": "ok", "model": "balanced 8-qubit 4-layer QML"}


@app.post("/predict/ecg")
def predict_ecg(request: EcgRequest) -> dict[str, Any]:
    try:
        explanation = explain_ecg(request.ecg, model_mode="balanced")
        return _build_response(explanation)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"ECG inference failed: {exc}") from exc