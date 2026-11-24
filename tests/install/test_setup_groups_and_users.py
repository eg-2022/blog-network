import subprocess
from unittest.mock import patch

from install.setup_groups_and_users import (
    check_if_group_created,
    create_maintainers_group,
)

@patch("install.setup_groups_and_users.grp.getgrnam")
@patch("builtins.print")
def test_check_if_group_created_returns_true(mock_print, mock_getgrnam):

    mock_getgrnam.return_value = True

    result = check_if_group_created()

    assert result is True
    mock_getgrnam.assert_called_once_with("maintainers")
    mock_print.assert_called_once()


@patch("install.setup_groups_and_users.grp.getgrnam")
def test_check_if_group_created_returns_none(mock_getgrnam):
    mock_getgrnam.side_effect = KeyError

    result = check_if_group_created()

    assert result is None


@patch("install.setup_groups_and_users.check_if_group_created", return_value=True)
@patch("install.setup_groups_and_users.subprocess.run")
def test_create_group_already_exists(mock_run, mock_check):
    result = create_maintainers_group()

    assert result is True
    mock_run.assert_not_called()


@patch("install.setup_groups_and_users.check_if_group_created", return_value=None)
@patch("install.setup_groups_and_users.subprocess.run")
@patch("builtins.print")
def test_create_group_success(mock_print, mock_run, mock_check):
    result = create_maintainers_group()

    assert result is True
    mock_run.assert_called_once_with(
        ["groupadd", "maintainers"],
        check=True,
        text=True,
        capture_output=True
    )


@patch("install.setup_groups_and_users.check_if_group_created", return_value=None)
@patch("install.setup_groups_and_users.subprocess.run")
@patch("builtins.print")
def test_create_group_file_not_found(mock_print, mock_run, mock_check):
    mock_run.side_effect = FileNotFoundError

    result = create_maintainers_group()

    assert result is False
    mock_print.assert_called_once()


@patch("install.setup_groups_and_users.check_if_group_created", return_value=None)
@patch("install.setup_groups_and_users.subprocess.run")
@patch("builtins.print")
def test_create_group_permission_error(mock_print, mock_run, mock_check):
    mock_run.side_effect = PermissionError

    result = create_maintainers_group()

    assert result is False
    mock_print.assert_called_once()


@patch("install.setup_groups_and_users.check_if_group_created", return_value=None)
@patch("install.setup_groups_and_users.subprocess.run")
@patch("builtins.print")
def test_create_group_called_process_error(
    mock_print, mock_run, mock_check
):
    mock_run.side_effect = subprocess.CalledProcessError(
        returncode=1,
        cmd=["groupadd", "maintainers"],
        stderr="Group already exists"
    )

    result = create_maintainers_group()

    assert result is False
    mock_print.assert_called_once()


@patch("install.setup_groups_and_users.check_if_group_created", return_value=None)
@patch("install.setup_groups_and_users.subprocess.run")
@patch("builtins.print")
def test_create_group_os_error(mock_print, mock_run, mock_check):
    mock_run.side_effect = OSError("Unexpected OS error")

    result = create_maintainers_group()

    assert result is False
    mock_print.assert_called_once()
