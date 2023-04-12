from test.data import get_path_to_parquet_as_pandas_requirements

import pytest
import toml  # type: ignore
from dac._input.pyproject import PyProjectConfig


@pytest.mark.parametrize("project_name,project_version", [("project_1", "0.1.2"), ("test_project", "6.6.6")])
def test_if_dependencies_are_passed_as_comma_separated_then_valid_pyproject_is_produced(
    project_name: str, project_version: str
):
    pm = PyProjectConfig(
        project_name=project_name,
        project_version=project_version,
        project_dependencies="pandas;adlfs; pyarrow",
    )
    toml_content = pm.generate_pyproject_toml()
    parsed_toml = toml.loads(toml_content)
    assert parsed_toml["project"]["name"] == pm.project_name
    assert parsed_toml["project"]["version"] == pm.project_version
    assert parsed_toml["project"]["dependencies"] == ["adlfs", "pandas", "pyarrow"]


@pytest.mark.parametrize("project_name,project_version", [("project_1", "0.1.2"), ("test_project", "6.6.6")])
def test_if_dependencies_are_passed_from_cat_requirements_then_valid_pyproject_is_produced(
    project_name: str, project_version: str
):
    pm = PyProjectConfig(
        project_name=project_name,
        project_version=project_version,
        project_dependencies=get_path_to_parquet_as_pandas_requirements().read_text(),
    )
    toml_content = pm.generate_pyproject_toml()
    parsed_toml = toml.loads(toml_content)
    assert parsed_toml["project"]["name"] == pm.project_name
    assert parsed_toml["project"]["version"] == pm.project_version
    assert parsed_toml["project"]["dependencies"] == [
        "pandas~=1.0",
        "pandera~=0.13.4",
        "pyarrow",
    ]


@pytest.mark.parametrize(
    "name",
    ["3nta"] + [f"in{c}valid" for c in [chr(i) for i in range(256)] if not c.isalnum() and c != "_" and c != "-"],
)
def test_if_invalid_project_name_then_raise_error(name: str):
    with pytest.raises(ValueError) as e:
        PyProjectConfig(
            project_name=name,
            project_version="0.1.2",
            project_dependencies="pandas,adlfs,pyarrow",
        )
    assert "Invalid project name" in str(e.value)


@pytest.mark.parametrize(
    "name",
    ["valid", "va_lid"],
)
def test_if_valid_project_name_then_dont_raise_error(name: str):
    PyProjectConfig(
        project_name=name,
        project_version="0.1.2",
        project_dependencies="pandas,adlfs,pyarrow",
    )
