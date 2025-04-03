from tempfile import TemporaryDirectory
from typing import Optional

from click.testing import Result
from typer.testing import CliRunner

from dac._cli import app
from dac._input.config import PackConfig
from test.data import (
    generate_random_project_name,
    get_path_to_self_contained_load_as_pandas,
    get_path_to_self_contained_schema,
    get_test_project_version,
)

runner = CliRunner()


def invoke_dac_pack(
    load: str = get_path_to_self_contained_load_as_pandas().as_posix(),
    schema: str = get_path_to_self_contained_schema().as_posix(),
    data: Optional[str] = None,
    output: Optional[str] = None,
    pkg_name: str = generate_random_project_name(),
    pkg_version: str = get_test_project_version(),
    pkg_dependencies: str = "pandas",
) -> Result:
    with TemporaryDirectory() as tmp_dir:
        if output is None:
            output = tmp_dir

        command = [
            "pack",
            "--load",
            load,
            "--schema",
            schema,
            "--output",
            output,
            "--pkg-name",
            pkg_name,
            "--pkg-version",
            pkg_version,
            "--pkg-dependencies",
            pkg_dependencies,
        ]
        if data is not None:
            command += ["--data", data]

        result = runner.invoke(
            app,
            command,
        )
    return result


def invoke_dac_pack_from_config(config: PackConfig) -> Result:
    return invoke_dac_pack(
        load=config.load_path.as_posix(),
        schema=config.schema_path.as_posix(),
        data=config.data_path.as_posix() if config.data_path is not None else None,
        output=config.wheel_dir.as_posix(),
        pkg_name=config.pyproject.project_name,
        pkg_version=config.pyproject.project_version,
        pkg_dependencies=config.pyproject.project_dependencies,
    )


def invoke_dac_next_version(
    pkg_name: str,
    major: Optional[int] = None,
) -> Result:
    major_option = [] if major is None else ["--major", str(major)]
    return runner.invoke(
        app,
        ["next-version", "--pkg-name", pkg_name] + major_option,
    )


def invoke_dac_info() -> Result:
    return runner.invoke(app, ["info"])
