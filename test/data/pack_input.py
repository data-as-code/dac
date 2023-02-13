import contextlib
from functools import partial
from pathlib import Path
from tempfile import TemporaryDirectory
from test.data import (
    generate_random_project_name,
    get_path_to_parquet_as_pandas_requirements,
    get_path_to_sample_load_parquet_as_pandas,
    get_path_to_sample_parquet,
    get_path_to_sample_schema,
    get_path_to_self_contained_load_as_pandas,
    get_path_to_self_contained_schema,
    get_test_project_version,
)
from typing import Generator, Optional

from dac._input.config import PackConfig
from dac._input.pyproject import PyProjectConfig


@contextlib.contextmanager
def _pack_input(
    data_path: Optional[Path],
    load_path: Path,
    schema_path: Path,
    wheel_dir,
    project_dependencies,
) -> Generator[PackConfig, None, None]:
    with TemporaryDirectory() as tmp_dir:
        pyproject = PyProjectConfig(
            project_name=generate_random_project_name(),
            project_version=get_test_project_version(),
            project_dependencies=project_dependencies,
        )
        config = PackConfig(
            data_path=data_path,
            load_path=load_path,
            schema_path=schema_path,
            wheel_dir=Path(tmp_dir) if wheel_dir is None else wheel_dir,
            pyproject=pyproject,
        )
        yield config


input_with_local_data = partial(
    _pack_input,
    data_path=get_path_to_sample_parquet(),
    load_path=get_path_to_sample_load_parquet_as_pandas(),
    schema_path=get_path_to_sample_schema(),
    wheel_dir=None,
    project_dependencies=get_path_to_parquet_as_pandas_requirements().read_text(),
)

input_with_self_contained_data = partial(
    _pack_input,
    data_path=None,
    load_path=get_path_to_self_contained_load_as_pandas(),
    schema_path=get_path_to_self_contained_schema(),
    wheel_dir=None,
    project_dependencies=get_path_to_parquet_as_pandas_requirements().read_text(),
)


# input_without_local_data = partial(
#     _pack_input,
#     data_path=None,
#     wheel_dir=None,
#     project_dependencies=get_path_to_parquet_as_pandas_requirements().read_text(),
# )
