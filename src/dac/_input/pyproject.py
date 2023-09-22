from dataclasses import dataclass
from typing import List

import toml  # type: ignore


@dataclass
class PyProjectConfig:
    project_name: str
    project_version: str
    project_dependencies: str

    def __post_init__(self):
        self.__check_project_name_is_valid()

    def __check_project_name_is_valid(self) -> None:
        if not self.project_name.isidentifier() or "\xb7" in self.project_name:
            raise ValueError(f"Invalid project name: {self.project_name} (hint: only '_' are allowed, no '-')")

    def generate_pyproject_toml(self) -> str:
        return toml.dumps(
            {
                "project": {
                    "name": self.project_name,
                    "version": self.project_version,
                    "dependencies": self._get_list_of_project_dependencies(),
                }
            }
        )

    def _get_list_of_project_dependencies(self) -> List[str]:
        splitted_by_newline = self.project_dependencies.splitlines()
        splitted_by_newline_or_comma = [s for ss in splitted_by_newline for s in ss.split(";")]
        return sorted(map(lambda x: x.strip(), splitted_by_newline_or_comma))
