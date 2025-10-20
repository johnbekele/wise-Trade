from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pandas as pd


@dataclass
class IngestionConfig:
    symbol: str
    start_date: Optional[str] = None  # YYYY-MM-DD
    end_date: Optional[str] = None    # YYYY-MM-DD
    raw_dir: Path = Path("ml/data/raw")


def fetch_prices(config: IngestionConfig) -> Path:
    """Fetch or generate OHLCV for a symbol and save to CSV under raw_dir.

    Replace the demo data generation with a real data source (e.g., Alpha Vantage).
    """
    config.raw_dir.mkdir(parents=True, exist_ok=True)
    out_path = config.raw_dir / f"{config.symbol}.csv"

    # Demo data: 100 rows of synthetic prices
    dates = pd.date_range(end=pd.Timestamp.today(), periods=100, freq="D")
    df = pd.DataFrame(
        {
            "date": dates,
            "open": pd.Series(range(100)).astype(float) + 100.0,
            "high": pd.Series(range(100)).astype(float) + 101.0,
            "low": pd.Series(range(100)).astype(float) + 99.0,
            "close": pd.Series(range(100)).astype(float) + 100.5,
            "volume": 1_000_000,
        }
    )
    df.to_csv(out_path, index=False)
    return out_path


