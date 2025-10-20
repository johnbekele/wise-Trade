#!/usr/bin/env python
from __future__ import annotations

import argparse
from pathlib import Path

from ml.ml_pipeline.ingestion import IngestionConfig, fetch_prices
from ml.ml_pipeline.preprocessing import PreprocessConfig, clean_prices
from ml.ml_pipeline.features import FeatureConfig, add_technical_features
from ml.ml_pipeline.training import TrainConfig, train_model
from ml.ml_pipeline.evaluation import EvalConfig, evaluate_model


def main() -> None:
    parser = argparse.ArgumentParser(description="Run ML pipeline end-to-end")
    parser.add_argument("--symbol", default="SPY", help="Ticker symbol to use")
    args = parser.parse_args()

    raw_csv = fetch_prices(IngestionConfig(symbol=args.symbol))
    processed_csv = clean_prices(raw_csv, PreprocessConfig())
    feature_csv = add_technical_features(processed_csv, FeatureConfig())
    model_path = train_model(feature_csv, TrainConfig())
    evaluate_model(feature_csv, model_path, EvalConfig())


if __name__ == "__main__":
    main()


