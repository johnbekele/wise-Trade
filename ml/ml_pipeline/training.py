from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


@dataclass
class TrainConfig:
    target_horizon: int = 1  # predict next-day up/down
    model_dir: Path = Path("ml/models")
    random_state: int = 42


def _build_supervised(df: pd.DataFrame, horizon: int) -> Tuple[np.ndarray, np.ndarray]:
    y = (df["close"].shift(-horizon) > df["close"]).astype(int)
    X = df[["return_1d", "sma_short", "sma_long"]].values
    # drop last rows with NaN target due to shift
    valid = ~y.isna()
    return X[valid.values], y[valid].astype(int).values


def train_model(feature_csv_path: Path, config: TrainConfig) -> Path:
    """Train a simple classifier to predict next-day direction."""
    config.model_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(feature_csv_path)
    X, y = _build_supervised(df, config.target_horizon)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=config.random_state, stratify=y
    )

    model = RandomForestClassifier(n_estimators=200, random_state=config.random_state)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Validation accuracy: {acc:.3f}")

    model_path = config.model_dir / "rf_direction.pkl"
    joblib.dump(model, model_path)
    return model_path


