from pathlib import Path

import pandas as pd


def load() -> pd.DataFrame:
    df = pd.read_parquet(Path(__file__).parent / "sample.parquet")
    df["datetime1"] = df["datetime1"].astype("datetime64[ns]")
    return df
