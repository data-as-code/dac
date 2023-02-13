from pathlib import Path

import pandas as pd


def load() -> pd.DataFrame:
    return pd.read_parquet(Path(__file__).parent / "sample.parquet")
