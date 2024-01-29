import pytest
from dac._version_management import increase_minor


def test_increase_minor_then_return_version_with_increased_minor():
    assert "0.6.0" == increase_minor(version="0.5.0")
    assert "0.6.0" == increase_minor(version="0.5.1rc0")


@pytest.mark.parametrize("version", ["0", "0.5", "guess.what.now", "guess.0.now"])
def test_if_invalid_version_then_increase_minor_raises_exception(version):
    with pytest.raises(Exception):
        increase_minor(version=version)
