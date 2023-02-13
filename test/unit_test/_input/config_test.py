from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from test.data import (
    get_path_to_invalid_load,
    get_path_to_invalid_schema,
    get_path_to_sample_load_parquet_as_pandas,
    get_path_to_sample_parquet,
    get_path_to_sample_schema,
    get_path_to_schema_incompatible_with_sample_df,
    get_path_to_self_contained_load_as_pandas,
    get_path_to_self_contained_schema,
)

import pytest
from pydantic import ValidationError

from dac._input.config import PackConfig
from dac._input.pyproject import PyProjectConfig


def test_if_all_valid_then_not_exceptions(pyproject: PyProjectConfig):
    with TemporaryDirectory() as tmp_dir:
        PackConfig(
            data_path=get_path_to_sample_parquet(),
            load_path=get_path_to_sample_load_parquet_as_pandas(),
            schema_path=get_path_to_sample_schema(),
            wheel_dir=Path(tmp_dir),
            pyproject=pyproject,
        )


def test_if_invalid_data_path_then_raise_exception(pyproject: PyProjectConfig):
    with TemporaryDirectory() as tmp_dir:
        with pytest.raises(ValidationError):
            PackConfig(
                data_path=Path("invalid/path"),
                load_path=get_path_to_sample_load_parquet_as_pandas(),
                schema_path=get_path_to_sample_schema(),
                wheel_dir=Path(tmp_dir),
                pyproject=pyproject,
            )


def test_if_invalid_wheel_dir_then_raise_exception(pyproject: PyProjectConfig):
    with NamedTemporaryFile() as tmp_file:
        with pytest.raises(ValidationError):
            PackConfig(
                data_path=Path(tmp_file.name),
                load_path=get_path_to_sample_load_parquet_as_pandas(),
                schema_path=get_path_to_sample_schema(),
                wheel_dir=Path("invalid/path"),
                pyproject=pyproject,
            )


def test_if_invalid_load_path_then_raise_exception(pyproject: PyProjectConfig):
    with TemporaryDirectory() as tmp_dir:
        with pytest.raises(ValidationError):
            PackConfig(
                data_path=get_path_to_sample_parquet(),
                load_path=Path("invalid/path"),
                schema_path=get_path_to_sample_schema(),
                wheel_dir=Path(tmp_dir),
                pyproject=pyproject,
            )


def test_if_load_does_not_contain_expected_function_then_raise_exception(pyproject: PyProjectConfig):
    with TemporaryDirectory() as tmp_dir:
        with pytest.raises(ValidationError):
            PackConfig(
                data_path=get_path_to_sample_parquet(),
                load_path=get_path_to_invalid_load(),
                schema_path=get_path_to_sample_schema(),
                wheel_dir=Path(tmp_dir),
                pyproject=pyproject,
            )


def test_if_invalid_schema_path_then_raise_exception(pyproject: PyProjectConfig):
    with TemporaryDirectory() as tmp_dir:
        with pytest.raises(ValidationError):
            PackConfig(
                data_path=get_path_to_sample_parquet(),
                load_path=get_path_to_sample_load_parquet_as_pandas(),
                schema_path=Path("invalid/path"),
                wheel_dir=Path(tmp_dir),
                pyproject=pyproject,
            )


def test_if_schema_does_not_contain_expected_class_then_raise_exception(pyproject: PyProjectConfig):
    with TemporaryDirectory() as tmp_dir:
        with pytest.raises(ValidationError):
            PackConfig(
                data_path=get_path_to_sample_parquet(),
                load_path=get_path_to_sample_load_parquet_as_pandas(),
                schema_path=get_path_to_invalid_schema(),
                wheel_dir=Path(tmp_dir),
                pyproject=pyproject,
            )


def test_if_data_path_is_not_provided_then_do_not_raise_exception(pyproject: PyProjectConfig):
    with TemporaryDirectory() as tmp_dir:
        PackConfig(
            load_path=get_path_to_self_contained_load_as_pandas(),
            schema_path=get_path_to_self_contained_schema(),
            wheel_dir=Path(tmp_dir),
            pyproject=pyproject,
        )


def test_if_schema_does_not_match_data_then_raise_exception(pyproject: PyProjectConfig):
    with TemporaryDirectory() as tmp_dir:
        with pytest.raises(ValidationError):
            PackConfig(
                data_path=get_path_to_sample_parquet(),
                load_path=get_path_to_sample_load_parquet_as_pandas(),
                schema_path=get_path_to_schema_incompatible_with_sample_df(),
                wheel_dir=Path(tmp_dir),
                pyproject=pyproject,
            )


@pytest.fixture(name="pyproject")
def fixture_pyproject() -> PyProjectConfig:
    return PyProjectConfig(
        project_name="test_project", project_version="0.1.2", project_dependencies="pandas,adlfs, pyarrow"
    )
