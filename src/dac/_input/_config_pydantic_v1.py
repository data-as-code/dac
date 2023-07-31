import importlib
import inspect
import sys
from pathlib import Path
from typing import Dict, Optional

import pandera as pa
from pydantic import BaseModel, root_validator, validator

from dac._file_helper import temporarily_copied_file
from dac._input.pyproject import PyProjectConfig


class PackConfig(BaseModel):
    data_path: Optional[Path] = None
    load_path: Path
    schema_path: Path
    wheel_dir: Path
    pyproject: PyProjectConfig

    @validator("data_path", "load_path", "schema_path", "wheel_dir")
    def path_exists(cls, path: Path) -> Path:  # pylint: disable=no-self-argument,no-self-use
        if path is not None and not path.exists():
            raise ValueError((f"Path {path.as_posix()} is not valid"))
        return path

    @validator("load_path")
    def load_contains_expected_function(cls, path: Path) -> Path:  # pylint: disable=no-self-argument,no-self-use
        try:
            sys.path.append(path.parent.as_posix())
            pkg = importlib.import_module(name=path.stem)
        except Exception as e:
            raise ValueError(
                (
                    f"{path.as_posix()} is not a path to a python module that can be imported, "
                    "because of the following error:"
                    "\n"
                    f"{e}"
                )
            ) from e

        try:
            signature = inspect.getfullargspec(pkg.load)
            assert signature.args == []
        except Exception as e:
            raise ValueError((f"{path.as_posix()} does not contain the required `def load()`")) from e
        return path

    @validator("schema_path")
    def schema_contains_expected_class(cls, path: Path) -> Path:  # pylint: disable=no-self-argument,no-self-use
        try:
            sys.path.append(path.parent.as_posix())
            pkg = importlib.import_module(name=path.stem)
        except Exception as e:
            raise ValueError(
                (
                    f"{path.as_posix()} is not a path to a python module that can be imported, "
                    "because of the following error:"
                    "\n"
                    f"{e}"
                )
            ) from e

        try:
            issubclass(pkg.Schema, pa.SchemaModel)
        except Exception as e:
            raise ValueError((f"{path.as_posix()} does not contain the required `class Schema(pa.SchemaModel)`")) from e
        return path

    @root_validator
    def schema_match_data(  # pylint: disable=no-self-argument,no-self-use
        cls, values: Dict[str, Path]
    ) -> Dict[str, Path]:
        try:
            sys.path.append(values["load_path"].parent.as_posix())
            load_module = importlib.import_module(name=values["load_path"].stem)
        except Exception as e:
            raise ValueError(
                "Validation of the schema against the data has failed because the load module could not be imported"
            ) from e

        try:
            if values.get("data_path", None) is not None:
                with temporarily_copied_file(
                    src=values["data_path"], dst=values["load_path"].parent / values["data_path"].name
                ):
                    data = load_module.load()
            else:
                data = load_module.load()
        except Exception as e:
            raise ValueError("`load()` failed due to the following error:" "\n" f"{e}") from e

        try:
            sys.path.append(values["schema_path"].parent.as_posix())
            schema_module = importlib.import_module(name=values["schema_path"].stem)
        except Exception as e:
            raise ValueError(
                "Validation of the schema against the data has failed because the schema module could not be imported"
            ) from e

        try:
            schema_module.Schema.validate(data, lazy=True)
        except pa.errors.SchemaErrors as e:
            raise ValueError("Validation of the schema against the data has failed:" "\n" f"{e.failure_cases}") from e
        except Exception as e:
            raise ValueError(
                "Validation of the schema against the data has failed for unexpected reasons:" "\n" f"{e}"
            ) from e

        return values
