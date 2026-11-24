
import pytest
from unittest.mock import patch
from pathlib import Path
import shutil

from install.install_sshd_config_files import (
    check_destination_directory,
    check_source_directory,
    copy_directory_to_source,
)

def test_check_source_directory_exists():
    with patch.object(Path, "exists", return_value=True):
        assert check_source_directory(Path("/fake/source")) is True


def test_check_source_directory_does_not_exist():
    with patch.object(Path, "exists", return_value=False):
        with pytest.raises(SystemExit) as exc:
            check_source_directory(Path("/fake/source"))

        assert exc.value.code == 1


def test_check_destination_directory_exists():
    with patch.object(Path, "exists", return_value=True):
        assert check_destination_directory(Path("/fake/destination")) is True


def test_check_destination_directory_does_not_exist():
    with patch.object(Path, "exists", return_value=False):
        with pytest.raises(SystemExit) as exc:
            check_destination_directory(Path("/fake/destination"))

        assert exc.value.code == 1


def test_copy_directory_successfully():
    with patch.object(shutil, "copytree") as mock_copy:
        result = copy_directory_to_source(
            "/fake/source",
            "/fake/destination"
        )

        assert result is True

        mock_copy.assert_called_once_with(
            src="/fake/source",
            dst="/fake/destination",
            dirs_exist_ok=True
        )


def test_copy_directory_file_not_found():
    with patch.object(
        shutil,
        "copytree",
        side_effect=FileNotFoundError("Directory not found")
    ):
        result = copy_directory_to_source(
            "/fake/source",
            "/fake/destination"
        )

        assert result is False


def test_copy_directory_not_a_directory():
    with patch.object(
        shutil,
        "copytree",
        side_effect=NotADirectoryError()
    ):
        result = copy_directory_to_source(
            "/fake/source",
            "/fake/destination"
        )

        assert result is False


def test_copy_directory_permission_error():
    with patch.object(
        shutil,
        "copytree",
        side_effect=PermissionError("Permission denied")
    ):
        result = copy_directory_to_source(
            "/fake/source",
            "/fake/destination"
        )

        assert result is None


def test_copy_directory_shutil_error():
    with patch.object(
        shutil,
        "copytree",
        side_effect=shutil.Error("Copy error")
    ):
        result = copy_directory_to_source(
            "/fake/source",
            "/fake/destination"
        )

        assert result is None


