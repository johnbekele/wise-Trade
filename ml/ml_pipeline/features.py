from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass
class FeatureConfig:
    window_short: int = 5
    window_long: int = 20


def add_technical_features(processed_csv_path: Path, config: FeatureConfig) -> Path:
    """Add simple moving averages and returns to processed prices CSV.

    Returns path to a new CSV with features appended.
    """
    df = pd.read_csv(processed_csv_path, parse_dates=["date"])  # ensure parse
    df = df.sort_values("date")
    df["return_1d"] = df["close"].pct_change().fillna(0.0)
    df["sma_short"] = df["close"].rolling(config.window_short).mean().bfill()
    df["sma_long"] = df["close"].rolling(config.window_long).mean().bfill()
    out_path = processed_csv_path.with_name(processed_csv_path.stem + "_features.csv")
    df.to_csv(out_path, index=False)
    return out_path


