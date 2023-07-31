from typing import List

import toml  # type: ignore
from pydantic import BaseModel, field_validator


class PyProjectConfig(BaseModel):
    project_name: str
    project_version: str
    project_dependencies: str

    @field_validator("project_name")
    @classmethod
    def valid_project_name(cls, name: str) -> str:  # pylint: disable=no-self-argument,no-self-use
        if not name.isidentifier() or "\xb7" in name:
            raise ValueError(f"Invalid project name: {name} (hint: only '_' are allowed, no '-')")
        return name

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
