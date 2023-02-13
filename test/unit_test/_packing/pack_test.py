from test.data.pack_input import input_with_self_contained_data
from unittest.mock import patch

from dac._packing import pack


def test_if_pack_then_first_prepare_project_dir_then_build_wheel():
    with patch("dac._packing.data_as_code_project") as data_as_code_project_mock, patch(
        "dac._packing.build_wheel"
    ) as build_wheel_mock:
        with input_with_self_contained_data() as config:
            pack(config=config)
        data_as_code_project_mock.assert_called_once_with(config=config)
        build_wheel_mock.assert_called_once_with(
            config=config, project_path=data_as_code_project_mock().__enter__.return_value
        )
