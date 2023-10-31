from pathlib import Path

import pandas as pd


def load(sample_n: int) -> pd.DataFrame:
    return pd.read_parquet(Path(__file__).parent / "sample.parquet").sample(n=sample_n)
