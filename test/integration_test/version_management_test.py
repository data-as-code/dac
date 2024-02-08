from test.cli_utilities import invoke_dac_next_version

import pytest
from dac._version_management import find_latest_version


def test_if_find_latest_version_is_called_then_return_latest_version():
    assert "0.5" == find_latest_version(pkg_name="rainbow-server")


def test_if_find_latest_version_is_called_with_major_constraint_then_return_latest_major_version():
    assert "0.25.3" == find_latest_version(pkg_name="pandas", major=0)


def test_if_pkg_does_not_exist_then_find_package_raises_exception():
    with pytest.raises(Exception):
        find_latest_version(pkg_name="non-existing-package")


def test_if_next_version_without_major_spec_then_return_latest_version_with_minor_upgrade():
    result = invoke_dac_next_version(pkg_name="rainbow-saddle")
    assert result.stdout == "0.5.0\n"


def test_if_next_version_with_major_spec_then_return_minor_upgrade_for_that_major():
    result = invoke_dac_next_version(pkg_name="pandas", major=0)
    assert result.stdout == "0.26.0\n"
