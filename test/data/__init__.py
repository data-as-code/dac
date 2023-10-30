import random
import string
from datetime import datetime
from pathlib import Path

import pandas as pd


def get_path_to_sample_parquet() -> Path:
    path = Path(__file__).parent / "parquet/sample.parquet"
    if not path.exists():
        get_sample_pandas_df().to_parquet(path=path)
    return path


def get_path_to_sample_load_parquet_as_pandas() -> Path:
    return Path(__file__).parent / "load/parquet_as_pandas.py"


def get_path_to_self_contained_load_as_pandas() -> Path:
    return Path(__file__).parent / "load/self_contained_as_pandas.py"


def get_path_to_invalid_load() -> Path:
    return Path(__file__).parent / "load/missing_load_function.py"


def get_path_to_missing_requirement_load() -> Path:
    return Path(__file__).parent / "load/missing_requirement.py"


def get_path_to_return_wrong_type_load() -> Path:
    return Path(__file__).parent / "load/return_wrong_type.py"


def get_path_to_sample_load_failing_because_of_missing_credentials() -> Path:
    return Path(__file__).parent / "load/missing_credentials.py"


def get_path_to_sample_schema() -> Path:
    return Path(__file__).parent / "schema/sample.py"


def get_path_to_sample_custom_schema() -> Path:
    return Path(__file__).parent / "schema/sample_custom.py"


def get_path_to_invalid_schema() -> Path:
    return Path(__file__).parent / "schema/invalid.py"


def get_path_to_schema_incompatible_with_sample_df() -> Path:
    return Path(__file__).parent / "schema/incompatible_with_sample_df.py"


def get_path_to_self_contained_schema() -> Path:
    return Path(__file__).parent / "schema/self_contained.py"


def get_path_to_wrong_syntax_schema() -> Path:
    return Path(__file__).parent / "schema/wrong_syntax.py"


def get_path_to_parquet_as_pandas_requirements() -> Path:
    return Path(__file__).parent / "requirements/parquet_as_pandas.txt"


def get_sample_pandas_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "int1": [1, 2, 3],
            "float1": [1.1 + 0.1 * i for i in range(3)],
            "string1": ["A", "B", "C"],
            "date1": [datetime(2023, 1, 1).date(), datetime(2023, 1, 1).date(), datetime(2023, 1, 1).date()],
            "datetime1": [
                datetime(2023, 1, 1, 12, 0, 0),
                datetime(2023, 1, 1, 12, 0, 1),
                datetime(2023, 1, 1, 12, 1, 0),
            ],
        }
    )


def generate_random_project_name() -> str:
    return "".join(random.choice(string.ascii_lowercase) for _ in range(16))


def get_test_project_version() -> str:
    return "1.2.3"
