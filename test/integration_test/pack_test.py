import contextlib
import subprocess
from importlib import import_module
from importlib.metadata import version
from pathlib import Path
from tempfile import TemporaryDirectory
from test.cli_utilities import invoke_dac_pack_from_config
from test.data import (
    generate_random_project_name,
    get_path_to_parquet_as_pandas_requirements,
    get_path_to_sample_load_parquet_as_pandas,
    get_path_to_sample_parquet,
    get_path_to_sample_schema,
    get_path_to_self_contained_load_as_pandas,
    get_path_to_self_contained_schema,
    get_sample_pandas_df,
    get_test_project_version,
)
from test.data.load import self_contained_as_pandas
from typing import Generator, Optional

import pandas as pd
import pandera as pa
import pytest

from dac import PackConfig, PyProjectConfig


@pytest.mark.slow
def test_if_valid_input_then_create_python_wheel():
    with _packed_data() as config:
        _verify_wheel(wheel_dir=Path(config.wheel_dir), pyproject=config.pyproject)


@pytest.mark.slow
def test_if_installed_then_can_load_data():
    with _packed_data() as config:
        files_in_wheel_dir = list(Path(config.wheel_dir).iterdir())
        with _pip_installed_wheel(path=files_in_wheel_dir[0]):
            pkg = import_module(config.pyproject.project_name)
            df = pkg.load()
            pd.testing.assert_frame_equal(get_sample_pandas_df(), df)


@pytest.mark.slow
def test_if_installed_then_can_access_schema():
    with _packed_data() as config:
        files_in_wheel_dir = list(Path(config.wheel_dir).iterdir())
        with _pip_installed_wheel(path=files_in_wheel_dir[0]):
            pkg = import_module(config.pyproject.project_name)
            assert issubclass(pkg.Schema, pa.SchemaModel)


@pytest.mark.slow
def test_if_data_embedded_in_load_then_load_returns_expected_data():
    with _packed_data(
        data_path=None,
        load_path=get_path_to_self_contained_load_as_pandas(),
        schema_path=get_path_to_self_contained_schema(),
    ) as config:
        files_in_wheel_dir = list(Path(config.wheel_dir).iterdir())
        with _pip_installed_wheel(path=files_in_wheel_dir[0]):
            pkg = import_module(config.pyproject.project_name)
            df = pkg.load()
            pd.testing.assert_frame_equal(self_contained_as_pandas.load(), df)


@contextlib.contextmanager
def _packed_data(
    data_path: Optional[Path] = get_path_to_sample_parquet(),
    load_path: Path = get_path_to_sample_load_parquet_as_pandas(),
    schema_path: Path = get_path_to_sample_schema(),
    project_dependencies: str = get_path_to_parquet_as_pandas_requirements().read_text(),
) -> Generator[PackConfig, None, None]:
    with TemporaryDirectory() as tmp_dir:
        config = PackConfig(
            data_path=data_path,
            load_path=load_path,
            schema_path=schema_path,
            wheel_dir=Path(tmp_dir),
            pyproject=PyProjectConfig(
                project_name=generate_random_project_name(),
                project_version=get_test_project_version(),
                project_dependencies=project_dependencies,
            ),
        )
        invoke_dac_pack_from_config(config=config)
        yield config


@contextlib.contextmanager
def _pip_installed_wheel(path: Path) -> Generator[None, None, None]:
    subprocess.run(
        ["python", "-m", "pip", "install", "--force-reinstall", path.as_posix()],
        check=True,
        capture_output=True,
    )
    try:
        yield None
    finally:
        subprocess.run(
            ["python", "-m", "pip", "uninstall", "-y", path.as_posix()],
            check=True,
            capture_output=True,
        )


def _verify_wheel(wheel_dir: Path, pyproject: PyProjectConfig) -> None:
    files_in_wheel_dir = list(Path(wheel_dir).iterdir())
    assert len(files_in_wheel_dir) == 1
    wheel_path = files_in_wheel_dir[0]
    assert wheel_path.suffix == ".whl"
    with _pip_installed_wheel(path=files_in_wheel_dir[0]):
        assert version(pyproject.project_name) == get_test_project_version()
