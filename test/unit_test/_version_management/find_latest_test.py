import subprocess
from test.data import get_pip_log_with_dash, get_pip_log_with_underscore
from unittest.mock import MagicMock

from dac._version_management import find_latest_version
from pytest import MonkeyPatch, fixture


def test_if_pkg_name_uses_dash_separator_and_pip_log_dash_then_correct_latest_version(mock_pip_output_with_dash: None):
    latest_version = find_latest_version(pkg_name="investing-algorithm-framework")
    assert latest_version == "2.3.2"


def test_if_pkg_name_uses_dash_separator_and_pip_log_underscore_then_correct_latest_version(
    mock_pip_output_with_underscore: None,
):
    latest_version = find_latest_version(pkg_name="investing-algorithm-framework")
    assert latest_version == "2.3.2"


def test_if_pkg_name_uses_underscore_separator_and_pip_log_dash_then_correct_latest_version(
    mock_pip_output_with_dash: None,
):
    latest_version = find_latest_version(pkg_name="investing_algorithm_framework")
    assert latest_version == "2.3.2"


def test_if_pkg_name_uses_underscore_separator_and_pip_log_underscore_then_correct_latest_version(
    mock_pip_output_with_underscore: None,
):
    latest_version = find_latest_version(pkg_name="investing_algorithm_framework")
    assert latest_version == "2.3.2"


@fixture
def mock_pip_output_with_dash(monkeypatch: MonkeyPatch):
    output = MagicMock()
    output.decode.return_value = get_pip_log_with_dash()

    def return_foo(*args, **kwargs) -> str:
        return output

    monkeypatch.setattr(subprocess, "check_output", return_foo)


@fixture
def mock_pip_output_with_underscore(monkeypatch: MonkeyPatch):
    output = MagicMock()
    output.decode.return_value = get_pip_log_with_underscore()

    def return_foo(*args, **kwargs) -> str:
        return output

    monkeypatch.setattr(subprocess, "check_output", return_foo)
