import filecmp
from test.data.pack_input import input_with_local_data, input_with_self_contained_data

from dac._packing import data_as_code_project
from dac._pyproject_factory import DaCProjectFactory


def test_if_provide_data_then_manifest_and_data_are_included_in_project_dir():
    with input_with_local_data() as config:
        assert config.data_path is not None
        with data_as_code_project(config=config) as proj_dir:
            assert (proj_dir / "MANIFEST.in").exists()
            project_data_path = proj_dir / "src" / config.pyproject.project_name / config.data_path.name
            assert project_data_path.exists()
            assert filecmp.cmp(config.data_path, project_data_path)


def test_if_dont_provide_data_then_manifest_is_not_included_in_project_dir():
    with input_with_self_contained_data() as config:
        with data_as_code_project(config=config) as proj_dir:
            assert not (proj_dir / "MANIFEST.in").exists()


def test_if_project_init_is_inspected_then_load_and_schema_is_found():
    with input_with_self_contained_data() as config:
        with data_as_code_project(config=config) as proj_dir:
            init_content = (proj_dir / "src" / config.pyproject.project_name / "__init__.py").read_text()
            assert f"from {config.pyproject.project_name}._load import load" in init_content
            assert f"from {config.pyproject.project_name}._schema import Schema" in init_content


def test_if_project_load_is_inspected_then_has_same_content_as_original():
    with input_with_self_contained_data() as config:
        with data_as_code_project(config=config) as proj_dir:
            project_load_path = proj_dir / "src" / config.pyproject.project_name / f"{DaCProjectFactory.load_file_name}"
            assert project_load_path.exists()
            assert filecmp.cmp(config.load_path, project_load_path)


def test_if_project_schema_is_inspected_then_has_same_content_as_original():
    with input_with_self_contained_data() as config:
        with data_as_code_project(config=config) as proj_dir:
            project_schema_path = (
                proj_dir / "src" / config.pyproject.project_name / f"{DaCProjectFactory.schema_file_name}"
            )
            assert project_schema_path.exists()
            assert filecmp.cmp(config.schema_path, project_schema_path)


def test_if_pyproject_is_inspected_then_content_comes_from_metadata_generation():
    with input_with_self_contained_data() as config:
        with data_as_code_project(config=config) as proj_dir:
            pyproject_path = proj_dir / "pyproject.toml"
            assert pyproject_path.exists()
            assert pyproject_path.read_text() == config.pyproject.generate_pyproject_toml()
