from test.data import get_pip_log_with_dash, get_pip_log_with_underscore
from unittest.mock import patch

from dac._version_management import find_latest_version


def test_if_pkg_name_uses_dash_separator_and_pip_log_dash_then_correct_latest_version():
    with patch("dac._version_management._pretend_pip_install") as mock_pretend_pip_install:
        mock_pretend_pip_install.return_value = get_pip_log_with_dash()

        latest_version = find_latest_version(pkg_name="investing-algorithm-framework")

        assert latest_version == "2.3.2"


def test_if_pkg_name_uses_dash_separator_and_pip_log_underscore_then_correct_latest_version():
    with patch("dac._version_management._pretend_pip_install") as mock_pretend_pip_install:
        mock_pretend_pip_install.return_value = get_pip_log_with_underscore()

        latest_version = find_latest_version(pkg_name="investing-algorithm-framework")

        assert latest_version == "2.3.2"


def test_if_pkg_name_uses_underscore_separator_and_pip_log_dash_then_correct_latest_version():
    with patch("dac._version_management._pretend_pip_install") as mock_pretend_pip_install:
        mock_pretend_pip_install.return_value = get_pip_log_with_dash()

        latest_version = find_latest_version(pkg_name="investing_algorithm_framework")

        assert latest_version == "2.3.2"


def test_if_pkg_name_uses_underscore_separator_and_pip_log_underscore_then_correct_latest_version():
    with patch("dac._version_management._pretend_pip_install") as mock_pretend_pip_install:
        mock_pretend_pip_install.return_value = get_pip_log_with_underscore()

        latest_version = find_latest_version(pkg_name="investing_algorithm_framework")

        assert latest_version == "2.3.2"
