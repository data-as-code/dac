import re
import subprocess
from typing import Optional


def find_latest_version(library_name: str, major: Optional[int] = None) -> str:
    output = subprocess.check_output(
        [
            "pip",
            "install",
            "--no-deps",
            "--ignore-installed",
            "--no-cache-dir",
            "--dry-run",
            f"{library_name}{f'=={major}.*' if major is not None else ''}",
        ],
        stderr=subprocess.DEVNULL,
    )
    last_line = output.decode("utf-8").splitlines()[-1]
    regex_rule = f"{library_name.replace('_', '-')}-{major if major is not None else ''}.[^ ]+"
    match = re.search(regex_rule, last_line)
    assert match is not None
    return match[0][len(f"{library_name}-") :]
