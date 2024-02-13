import re
import subprocess
from typing import Optional


def find_latest_version(pkg_name: str, major: Optional[int] = None) -> str:
    output = subprocess.check_output(
        [
            "pip",
            "install",
            "--no-deps",
            "--ignore-installed",
            "--no-cache-dir",
            "--dry-run",
            f"{pkg_name}{f'=={major}.*' if major is not None else ''}",
        ],
        stderr=subprocess.DEVNULL,
    )
    output_lines = output.decode("utf-8").splitlines()
    would_install_line = [line for line in output_lines if "Would install" in line][0]
    regex_rule = f"{pkg_name.replace('_', '-')}-{major if major is not None else ''}.[^ ]+"
    match = re.search(regex_rule, would_install_line.replace("_", "-"))
    assert match is not None
    return match[0][len(f"{pkg_name}-") :]


def increase_minor(version: str) -> str:
    major, minor, patch = version.split(".")
    assert major.isdigit() and minor.isdigit()
    return f"{major}.{int(minor) + 1}.0"
