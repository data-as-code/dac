from importlib.metadata import version

import dac
from test.cli_utilities import invoke_dac_info


def test_if_invoke_dac_info_from_shell_then_do_not_raise_error():
    result = invoke_dac_info()
    assert result.exit_code == 0


def test_if_dac_info_then_result_contains_dac_version():
    result = invoke_dac_info()
    assert version(dac.__name__) in result.stdout
