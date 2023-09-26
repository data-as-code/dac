import importlib
import inspect
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pandera as pa

from dac._file_helper import temporarily_copied_file
from dac._input.pyproject import PyProjectConfig


@dataclass
class PackConfig:
    load_path: Path
    schema_path: Path
    wheel_dir: Path
    pyproject: PyProjectConfig
    data_path: Optional[Path] = None

    def __post_init__(self):
        map(PackConfig._check_path_exists, (self.load_path, self.schema_path, self.wheel_dir, self.data_path))
        self._check_load_contains_expected_function()
        self._check_schema_contains_expected_class()
        self._check_schema_match_data()

    @staticmethod
    def _check_path_exists(path: Optional[Path]) -> None:
        if path is not None and not path.exists():
            raise ValueError((f"Path {path.as_posix()} is not valid"))

    def _check_load_contains_expected_function(self) -> None:
        try:
            sys.path.append(self.load_path.parent.as_posix())
            pkg = importlib.import_module(name=self.load_path.stem)
        except Exception as e:
            raise ValueError(
                (
                    f"{self.load_path.as_posix()} is not a path to a python module that can be imported, "
                    "because of the following error:"
                    "\n"
                    f"{e}"
                )
            ) from e

        try:
            signature = inspect.getfullargspec(pkg.load)
            assert signature.args == []
        except Exception as e:
            raise ValueError((f"{self.load_path.as_posix()} does not contain the required `def load()`")) from e

    def _check_schema_contains_expected_class(self) -> None:
        try:
            sys.path.append(self.schema_path.parent.as_posix())
            pkg = importlib.import_module(name=self.schema_path.stem)
        except Exception as e:
            raise ValueError(
                (
                    f"{self.schema_path.as_posix()} is not a path to a python module that can be imported, "
                    "because of the following error:"
                    "\n"
                    f"{e}"
                )
            ) from e

        try:
            issubclass(pkg.Schema, pa.SchemaModel)
        except Exception as e:
            raise ValueError(
                (f"{self.schema_path.as_posix()} does not contain the required `class Schema(pa.SchemaModel)`")
            ) from e

    def _check_schema_match_data(self) -> None:
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
