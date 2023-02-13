import shutil
from contextlib import contextmanager
from pathlib import Path
from typing import Generator


@contextmanager
def temporarily_copied_file(src: Path, dst: Path) -> Generator[None, None, None]:
    if src != dst:
        shutil.copyfile(src=src, dst=dst)
        try:
            yield None
        finally:
            dst.unlink()
    else:
        yield None
