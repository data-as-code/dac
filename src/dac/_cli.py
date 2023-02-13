import platform
import sys
from importlib.metadata import requires, version
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

import dac
from dac._input.config import PackConfig
from dac._input.pyproject import PyProjectConfig
from dac._packing import pack as py_api_pack

app = typer.Typer()
console = Console()


@app.command()
def pack(
    load_path: Path = typer.Option(
        Path("./load.py"),
        "--load",
        help="Path to python file containing the load function",
        rich_help_panel="Input code",
    ),
    schema_path: Path = typer.Option(
        Path("./schema.py"),
        "--schema",
        help="Path to python file containing the pandera SchemaModel",
        rich_help_panel="Input code",
    ),
    data_path: Path = typer.Option(
        None,
        "--data",
        help="Path to one single data file that should be bundled in the python wheel. "
        "It will be accessible in `Path(__file__).parent` by load",
        rich_help_panel="Optional input data",
    ),
    pkg_name: str = typer.Option(
        ..., help="Name of the python package contained in the wheel", rich_help_panel="Package config"
    ),
    pkg_version: str = typer.Option(
        ..., help="Version of the python package contained in the wheel", rich_help_panel="Package config"
    ),
    pkg_dependencies: str = typer.Option(
        ...,
        help="Dependencies needed to install the python wheel. "
        "Separator can either be comma (e.g. `'pandas, pandera[io]'`) "
        'or newline (e.g. `"$(cat requirements.txt)"`)',
        rich_help_panel="Package config",
    ),
    wheel_dir: Path = typer.Option(Path(), "--output", help="Path to the output directory", rich_help_panel="Output"),
):
    """
    Build a Data as Code (DaC) python wheel after verifying that data
    can be loaded and that data respect the provided schema.
    """
    py_api_pack(
        config=PackConfig(
            data_path=data_path,
            load_path=load_path,
            schema_path=schema_path,
            wheel_dir=wheel_dir,
            pyproject=PyProjectConfig(
                project_name=pkg_name, project_version=pkg_version, project_dependencies=pkg_dependencies
            ),
        ),
    )


@app.command()
def info():
    """
    Print information about the dac installation
    """
    table = Table("Name", "Version")
    table.add_row(dac.__name__, version(dac.__name__))
    requirements = requires(dac.__name__)
    assert requirements is not None
    for r in requirements:
        lib_name = r.split(" ")[0]
        table.add_row(lib_name, version(lib_name.split("[")[0]))
    table.add_row("python", sys.version)
    table.add_row("platform", platform.platform())
    console.print(table)


if __name__ == "__main__":
    app()
