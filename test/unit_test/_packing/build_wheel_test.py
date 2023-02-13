from unittest.mock import MagicMock, patch

from dac._packing import build_wheel


def test_if_invoked_then_build_is_called_from_cli():
    with patch("dac._packing.run") as run_mock:
        config_mock = MagicMock()
        project_path_mock = MagicMock()
        build_wheel(config=config_mock, project_path=project_path_mock)
        run_mock.assert_called_once()
        _, args, _ = run_mock.mock_calls[0]
        assert args[0] == [
            "python",
            "-m",
            "build",
            "--wheel",
            "--outdir",
            config_mock.wheel_dir.as_posix.return_value,
            project_path_mock.as_posix.return_value,
        ]
