from contextlib import contextmanager
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory
from typing import Generator

from dac._input.config import PackConfig
from dac._pyproject_factory import DaCProjectFactory


def pack(config: PackConfig) -> None:
    with data_as_code_project(config=config) as project_path:
        build_wheel(config=config, project_path=project_path)


@contextmanager
def data_as_code_project(config: PackConfig) -> Generator[Path, None, None]:
    with TemporaryDirectory() as tmp_dir:
        project_path = Path(tmp_dir)
        _prepare_project_dir(project_dir=project_path, config=config)
        yield project_path


def build_wheel(config: PackConfig, project_path: Path) -> None:
    run(
        ["python", "-m", "build", "--wheel", "--outdir", config.wheel_dir.as_posix(), project_path.as_posix()],
        check=True,
        capture_output=True,
    )


def _prepare_project_dir(project_dir: Path, config: PackConfig) -> None:
    dac_project_dir = DaCProjectFactory(
        project_dir=project_dir,
        load_path=config.load_path,
        schema_path=config.schema_path,
        project_name=config.pyproject.project_name,
        pyproject_toml=config.pyproject.generate_pyproject_toml(),
    )
    if config.data_path is not None:
        dac_project_dir.add_data(data_path=config.data_path)
