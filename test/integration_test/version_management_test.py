import pytest
from dac._version_management import find_latest_version


def test_if_find_latest_version_is_called_then_return_latest_version():
    assert "0.5" == find_latest_version(library_name="rainbow-server")


def test_if_find_latest_version_is_called_with_major_constraint_then_return_latest_major_version():
    assert "0.25.3" == find_latest_version(library_name="pandas", major=0)


def test_if_pkg_does_not_exist_then_find_package_return_none():
    with pytest.raises(Exception):
        find_latest_version(library_name="non-existing-package")
