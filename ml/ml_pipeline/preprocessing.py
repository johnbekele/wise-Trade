from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass
class PreprocessConfig:
    processed_dir: Path = Path("ml/data/processed")


def clean_prices(raw_csv_path: Path, config: PreprocessConfig) -> Path:
    """Load raw csv, parse dates, sort, drop na, save cleaned csv."""
    config.processed_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(raw_csv_path)
    df["date"] = pd.to_datetime(df["date"])  # ensure datetime
    df = df.sort_values("date").dropna()
    out_path = config.processed_dir / raw_csv_path.name
    df.to_csv(out_path, index=False)
    return out_path


