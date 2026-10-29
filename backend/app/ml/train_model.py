"""
PlacePilot – Random Forest Training Pipeline

NOTE: This module uses SYNTHETIC/DEMO training data because no real
historical placement dataset is available. Results from this model
are prototype outputs and do NOT represent real-world placement outcomes.

The code is structured so a real dataset can replace the synthetic data
by changing the `load_dataset()` function.
"""
import os
import json
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report
)
from pathlib import Path

# ── Constants ──────────────────────────────────────────────────────────────────
FEATURES = [
    "academic_score",
    "dsa_score",
    "programming_score",
    "dbms_score",
    "oop_score",
    "aptitude_score",
    "coding_score",
    "technical_score",
    "interview_score",
    "resume_score",
    "leetcode_score",
    "communication_score",
]

TARGET = "readiness_category"
CLASSES = ["Ready", "Moderately Ready", "Needs Improvement"]
MODEL_DIR = Path(__file__).parent / "models"


def generate_synthetic_dataset(n_samples: int = 800) -> pd.DataFrame:
    """
    Generate synthetic training data.
    
    """
    np.random.seed(42)
    rows = []

    for _ in range(n_samples):
        # Simulate different student archetypes
        archetype = np.random.choice(["strong", "average", "weak"], p=[0.3, 0.45, 0.25])

        if archetype == "strong":
            base = np.random.uniform(70, 95)
            label = "Ready" if base > 80 else "Moderately Ready"
        elif archetype == "average":
            base = np.random.uniform(50, 75)
            label = "Moderately Ready" if base > 60 else "Needs Improvement"
        else:
            base = np.random.uniform(30, 60)
            label = "Needs Improvement" if base < 50 else "Moderately Ready"

        noise = lambda: np.random.normal(0, 8)
        academic = np.clip(base * 0.85 + noise(), 20, 100)

        row = {
            "academic_score":    np.clip(academic, 20, 100),
            "dsa_score":         np.clip(base + noise(), 10, 100),
            "programming_score": np.clip(base + noise(), 10, 100),
            "dbms_score":        np.clip(base - 5 + noise(), 10, 100),
            "oop_score":         np.clip(base + noise(), 10, 100),
            "aptitude_score":    np.clip(base + 2 + noise(), 10, 100),
            "coding_score":      np.clip(base + noise(), 10, 100),
            "technical_score":   np.clip(base - 3 + noise(), 10, 100),
            "interview_score":   np.clip(base - 8 + noise(), 10, 100),
            "resume_score":      np.clip(base - 2 + noise(), 10, 100),
            "leetcode_score":    np.clip(base - 5 + noise(), 10, 100),
            "communication_score": np.clip(base - 4 + noise(), 10, 100),
            TARGET:              label,
        }
        rows.append(row)

    df = pd.DataFrame(rows)
    print(f"[ML] Generated {len(df)} synthetic samples")
    print(f"[ML] Label distribution:\n{df[TARGET].value_counts()}")
    return df


def load_dataset() -> pd.DataFrame:
    """
    Load dataset. Returns synthetic data for prototype.
    To use real data, replace this function body with:
        return pd.read_csv("your_placement_dataset.csv")
    """
    real_data_path = MODEL_DIR.parent / "real_dataset.csv"
    if real_data_path.exists():
        print(f"[ML] Loading real dataset from {real_data_path}")
        return pd.read_csv(real_data_path)

    print("[ML] No real dataset found. Using SYNTHETIC demo data.")
    return generate_synthetic_dataset()


def train_and_save():
    """Full training pipeline: load → preprocess → train → evaluate → save."""
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Load data
    df = load_dataset()

    # 2. Encode target
    le = LabelEncoder()
    le.fit(CLASSES)
    df["label_encoded"] = le.transform(df[TARGET])

    # 3. Features / target
    X = df[FEATURES].values
    y = df["label_encoded"].values

    # 4. Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 5. Train Random Forest
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        class_weight="balanced",
    )
    model.fit(X_train, y_train)
    print("[ML] Random Forest training complete")

    # 6. Evaluate
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average="weighted", zero_division=0)
    rec = recall_score(y_test, y_pred, average="weighted", zero_division=0)
    f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)
    cm = confusion_matrix(y_test, y_pred).tolist()

    print(f"[ML] Accuracy:  {acc:.3f}")
    print(f"[ML] Precision: {prec:.3f}")
    print(f"[ML] Recall:    {rec:.3f}")
    print(f"[ML] F1:        {f1:.3f}")

    eval_results = {
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1_score": round(f1, 4),
        "confusion_matrix": cm,
        "class_labels": list(le.classes_),
        "training_samples": len(X_train),
        "test_samples": len(X_test),
        "features": FEATURES,
        "is_demo_data": True,
        "note": "Demo model – evaluation based on synthetic data. Replace with real dataset for production.",
    }

    # 7. Save model, encoder, and evaluation
    joblib.dump(model, MODEL_DIR / "random_forest_model.pkl")
    joblib.dump(le, MODEL_DIR / "label_encoder.pkl")
    with open(MODEL_DIR / "evaluation.json", "w") as f:
        json.dump(eval_results, f, indent=2)

    print(f"[ML] Model saved to {MODEL_DIR}")
    return model, le, eval_results


# Run if called directly
if __name__ == "__main__":
    train_and_save()
