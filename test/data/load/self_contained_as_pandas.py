import pandas as pd


def load() -> pd.DataFrame:
    return pd.DataFrame({"A": [1, 2, 3], "B": [0.1, 0.2, 0.3]})
