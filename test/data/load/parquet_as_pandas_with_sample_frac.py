from pathlib import Path

import pandas as pd


def load(sample_frac: float = 1.0) -> pd.DataFrame:
    return pd.read_parquet(Path(__file__).parent / "sample.parquet").sample(frac=sample_frac)
