from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report


@dataclass
class EvalConfig:
    horizon: int = 1


def evaluate_model(feature_csv_path: Path, model_path: Path, config: EvalConfig) -> None:
    df = pd.read_csv(feature_csv_path)
    y = (df["close"].shift(-config.horizon) > df["close"]).astype(int)
    X = df[["return_1d", "sma_short", "sma_long"]].values
    valid = ~y.isna()
    X, y = X[valid.values], y[valid].astype(int).values

    model = joblib.load(model_path)
    preds = model.predict(X)
    print(classification_report(y, preds, digits=3))


