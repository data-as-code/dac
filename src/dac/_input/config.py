import importlib
import inspect
import sys
from pathlib import Path
from typing import Optional

import pandera as pa
from pydantic import BaseModel, field_validator, model_validator

from dac._file_helper import temporarily_copied_file
from dac._input.pyproject import PyProjectConfig


class PackConfig(BaseModel):
    data_path: Optional[Path] = None
    load_path: Path
    schema_path: Path
    wheel_dir: Path
    pyproject: PyProjectConfig

    @field_validator("data_path", "load_path", "schema_path", "wheel_dir")
    @classmethod
    def path_exists(cls, path: Path) -> Path:  # pylint: disable=no-self-argument,no-self-use
        if path is not None and not path.exists():
            raise ValueError((f"Path {path.as_posix()} is not valid"))
        return path

    @field_validator("load_path")
    @classmethod
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

    @field_validator("schema_path")
    @classmethod
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

    @model_validator(mode="after")
    def schema_match_data(self) -> "PackConfig":
        try:
            sys.path.append(self.load_path.parent.as_posix())
            load_module = importlib.import_module(name=self.load_path.stem)
        except Exception as e:
            raise ValueError(
                "Validation of the schema against the data has failed because the load module could not be imported"
            ) from e

        try:
            if self.data_path is not None:
                with temporarily_copied_file(src=self.data_path, dst=self.load_path.parent / self.data_path.name):
                    data = load_module.load()
            else:
                data = load_module.load()
        except Exception as e:
            raise ValueError("`load()` failed due to the following error:" "\n" f"{e}") from e

        try:
            sys.path.append(self.schema_path.parent.as_posix())
            schema_module = importlib.import_module(name=self.schema_path.stem)
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

        return self
