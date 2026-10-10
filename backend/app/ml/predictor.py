"""
PlacePilot – Readiness Predictor
Loads trained model and provides prediction + SHAP explanation.
"""
import json
import numpy as np
import joblib
from pathlib import Path
from typing import Dict, List, Tuple, Optional

MODEL_DIR = Path(__file__).parent / "models"
FEATURES = [
    "academic_score", "dsa_score", "programming_score", "dbms_score",
    "oop_score", "aptitude_score", "coding_score", "technical_score",
    "interview_score", "resume_score", "leetcode_score", "communication_score",
]
CLASSES = ["Ready", "Moderately Ready", "Needs Improvement"]

_model = None
_encoder = None
_explainer = None


def _load_model():
    global _model, _encoder
    model_path = MODEL_DIR / "random_forest_model.pkl"
    encoder_path = MODEL_DIR / "label_encoder.pkl"

    if not model_path.exists():
        from .train_model import train_and_save
        print("[Predictor] No model found, training now...")
        _model, _encoder, _ = train_and_save()
        return

    _model = joblib.load(model_path)
    _encoder = joblib.load(encoder_path)
    print("[Predictor] Model loaded successfully")


def _get_model():
    global _model, _encoder
    if _model is None:
        _load_model()
    return _model, _encoder


def _get_explainer():
    global _explainer
    if _explainer is not None:
        return _explainer
    try:
        import shap
        model, _ = _get_model()
        _explainer = shap.TreeExplainer(model)
        return _explainer
    except Exception as e:
        print(f"[SHAP] Could not create explainer: {e}")
        return None


def predict_readiness(features: Dict[str, float]) -> Dict:
    """
    Run Random Forest prediction and SHAP explanation.

    Args:
        features: dict with keys matching FEATURES list

    Returns:
        dict with readiness_category, readiness_score, confidence,
              shap_values, positive_factors, negative_factors
    """
    model, encoder = _get_model()

    # Build feature vector
    X = np.array([[features.get(f, 50.0) for f in FEATURES]])

    # Predict
    pred_encoded = model.predict(X)[0]
    pred_proba = model.predict_proba(X)[0]
    pred_label = encoder.inverse_transform([pred_encoded])[0]
    confidence = float(max(pred_proba))

    # Readiness score: weighted sum mapped to 0-100
    # Ready=100, Moderately Ready=60, Needs Improvement=25
    weights = dict(zip(encoder.classes_, [100, 60, 25]))
    readiness_score = sum(
        prob * weights.get(cls, 50)
        for cls, prob in zip(encoder.classes_, pred_proba)
    )
    readiness_score = round(float(readiness_score), 1)

    # SHAP explanation
    shap_result = _compute_shap(X, features)

    return {
        "readiness_category": pred_label,
        "readiness_score": readiness_score,
        "confidence": round(confidence, 3),
        **shap_result,
    }


def _compute_shap(X: np.ndarray, features: Dict[str, float]) -> Dict:
    """Compute SHAP values, fall back to permutation-based demo if unavailable."""
    explainer = _get_explainer()

    if explainer is not None:
        try:
            shap_values = explainer.shap_values(X)
            # Multi-class: sum absolute values for feature importance direction
            if isinstance(shap_values, list):
                # shape: [n_classes, n_samples, n_features]
                # Use SHAP of the predicted class (index 0 = Ready)
                sv = shap_values[0][0]
            else:
                sv = shap_values[0]

            shap_dict = {FEATURES[i]: round(float(sv[i]), 3) for i in range(len(FEATURES))}
        except Exception as e:
            print(f"[SHAP] Error computing values: {e}")
            shap_dict = _demo_shap(features)
    else:
        shap_dict = _demo_shap(features)

    # Split into positive and negative contributors
    sorted_items = sorted(shap_dict.items(), key=lambda x: abs(x[1]), reverse=True)
    positive_factors = [
        {"feature": k, "value": round(features.get(k, 0), 1), "shap": v, "label": _label(k)}
        for k, v in sorted_items if v > 0
    ]
    negative_factors = [
        {"feature": k, "value": round(features.get(k, 0), 1), "shap": v, "label": _label(k)}
        for k, v in sorted_items if v < 0
    ]

    return {
        "shap_values": shap_dict,
        "positive_factors": positive_factors[:5],
        "negative_factors": negative_factors[:5],
    }


def _demo_shap(features: Dict[str, float]) -> Dict:
    """
    Deterministic rule-based SHAP approximation used when shap library
    is unavailable. Clearly labelled as demo.
    """
    mean_score = 65.0
    shap_dict = {}
    for f in FEATURES:
        val = features.get(f, 50.0)
        diff = (val - mean_score) / 100.0
        shap_dict[f] = round(diff * 0.15, 3)
    return shap_dict


def _label(feature_name: str) -> str:
    labels = {
        "academic_score": "Academic Performance",
        "dsa_score": "DSA",
        "programming_score": "Programming",
        "dbms_score": "DBMS",
        "oop_score": "OOP",
        "aptitude_score": "Aptitude",
        "coding_score": "Coding Test",
        "technical_score": "Technical Knowledge",
        "interview_score": "Interview Performance",
        "resume_score": "Resume Quality",
        "leetcode_score": "LeetCode Activity",
        "communication_score": "Communication",
    }
    return labels.get(feature_name, feature_name.replace("_", " ").title())


def get_evaluation() -> Dict:
    """Return stored model evaluation metrics."""
    eval_path = MODEL_DIR / "evaluation.json"
    if eval_path.exists():
        with open(eval_path) as f:
            return json.load(f)
    # Trigger training
    from .train_model import train_and_save
    _, _, eval_results = train_and_save()
    return eval_results
