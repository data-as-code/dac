import subprocess


def test_if_invoke_dac_help_from_shell_then_do_not_raise_error():
    subprocess.run(["dac", "--help"], check=True)
