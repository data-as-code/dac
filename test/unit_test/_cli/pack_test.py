from importlib import import_module
from inspect import signature
from unittest.mock import MagicMock, patch

import pytest
from click.testing import Result

from dac._input.config import PackConfig
from test.cli_utilities import invoke_dac_pack
from test.data import (
    get_path_to_missing_requirement_load,
    get_path_to_return_wrong_type_load,
    get_path_to_sample_load_failing_because_of_missing_credentials,
    get_path_to_sample_schema,
    get_path_to_wrong_syntax_schema,
)
from test.data.pack_input import input_with_local_data, input_with_self_contained_data


@pytest.fixture(autouse=True)
def fixture_ensure_pack_signautre():
    pack_signature = signature(import_module("dac._cli").py_api_pack)
    assert len(pack_signature.parameters) == 1
    assert pack_signature.parameters["config"].annotation == PackConfig


@patch("dac._cli.py_api_pack")
def test_if_dac_pack_without_data_then_call_pack_with_expected_input(pack_mock):
    with input_with_self_contained_data() as config:
        result = _invoke_dac_pack_from_config(config=config)

    assert result.exit_code == 0
    pack_mock.assert_called_once_with(config=config)


@patch("dac._cli.py_api_pack")
def test_if_dac_pack_with_data_then_call_pack_with_expected_input(pack_mock: MagicMock):
    with input_with_local_data() as config:
        result = _invoke_dac_pack_from_config(config=config)

    assert result.exit_code == 0
    pack_mock.assert_called_once_with(config=config)


def test_if_data_does_not_match_schema_error_contains_pandera_error_info():
    result = invoke_dac_pack(schema=get_path_to_sample_schema().as_posix())
    assert result.exit_code != 0
    error_message = str(result.exception)
    assert "int1" in error_message
    assert "float1" in error_message
    assert "string1" in error_message
    assert "date1" in error_message
    assert "datetime1" in error_message


def test_if_load_requires_missing_requirement_then_error_contains_meaningful_info():
    result = invoke_dac_pack(load=get_path_to_missing_requirement_load().as_posix())
    assert result.exit_code != 0
    error_message = str(result.exception)
    assert "No module named 'modin'" in error_message


def test_if_load_returns_wrong_type_then_error_contains_meaningful_info():
    result = invoke_dac_pack(load=get_path_to_return_wrong_type_load().as_posix())
    assert result.exit_code != 0
    error_message = str(result.exception)
    assert "pandas" in error_message or "pd.DataFrame" in error_message


def test_if_load_miss_credentials_then_error_contains_meaningful_info():
    result = invoke_dac_pack(load=get_path_to_sample_load_failing_because_of_missing_credentials().as_posix())
    assert result.exit_code != 0
    error_message = str(result.exception)
    assert "Missing credentials" in error_message


def test_if_schema_has_wrong_syntax_then_error_contains_meningful_info():
    result = invoke_dac_pack(schema=get_path_to_wrong_syntax_schema().as_posix())
    assert result.exit_code != 0
    error_message = str(result.exception)
    assert "invalid" in error_message


def _invoke_dac_pack_from_config(config: PackConfig) -> Result:
    return invoke_dac_pack(
        load=config.load_path.as_posix(),
        schema=config.schema_path.as_posix(),
        data=None if config.data_path is None else config.data_path.as_posix(),
        output=config.wheel_dir.as_posix(),
        pkg_name=config.pyproject.project_name,
        pkg_version=config.pyproject.project_version,
        pkg_dependencies=config.pyproject.project_dependencies,
    )
