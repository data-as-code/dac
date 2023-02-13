import shutil
from pathlib import Path


class DaCProjectFactory:
    load_file_name = "_load.py"
    schema_file_name = "_schema.py"

    def __init__(self, project_dir: Path, load_path: Path, schema_path: Path, project_name: str, pyproject_toml: str):
        self._project_dir = project_dir
        self._load_path = load_path
        self._schema_path = schema_path
        self._project_name = project_name
        self._pyproject_toml = pyproject_toml

        self._init_dir()
        self._add_load()
        self._add_schema()

    def add_data(self, data_path: Path) -> None:
        manifest_path = self._project_dir / "MANIFEST.in"
        manifest_content = manifest_path.read_text() if manifest_path.exists() else ""
        manifest_content_to_add = f"global-include *{data_path.suffix}"
        if manifest_content_to_add not in manifest_content:
            manifest_path.write_text("\n".join([manifest_content, manifest_content_to_add]))

        shutil.copyfile(src=data_path, dst=self._project_dir / "src" / self._project_name / data_path.name)

    def _init_dir(self):
        (self._project_dir / "src" / self._project_name).mkdir(parents=True)
        (self._project_dir / "src" / self._project_name / "__init__.py").write_text(self._generate_pkg_init_content())
        (self._project_dir / "pyproject.toml").write_text(self._pyproject_toml)

    def _add_load(self):
        shutil.copyfile(src=self._load_path, dst=self._project_dir / "src" / self._project_name / self.load_file_name)

    def _add_schema(self):
        shutil.copyfile(
            src=self._schema_path, dst=self._project_dir / "src" / self._project_name / self.schema_file_name
        )

    def _generate_pkg_init_content(self) -> str:
        return "\n".join(
            [
                f"from {self._project_name}.{self.load_file_name[:-3]} import load  # noqa: F401",
                f"from {self._project_name}.{self.schema_file_name[:-3]} import Schema  # noqa: F401",
            ]
        )
