import modin.config as modin_cfg
import pandas as pd


def load() -> pd.DataFrame:
    modin_cfg.Engine.put("dask")
    return pd.DataFrame({"A": [1, 2, 3], "B": [0.1, 0.2, 0.3]})
