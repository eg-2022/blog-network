from unittest.mock import patch

from preinstall import check_if_debian_or_ubuntu


def test_check_if_debian_or_ubuntu_returns_true():
    with patch(
        "preinstall.check_if_debian_or_ubuntu.platform.freedesktop_os_release",
        return_value={"ID": "debian"}
    ):
        assert check_if_debian_or_ubuntu() is True


def test_check_if_debian_or_ubuntu_returns_false():
    with patch(
        "preinstall.check_if_debian_or_ubuntu.platform.freedesktop_os_release",
        return_value={"ID": "fedora"}
    ):
        assert check_if_debian_or_ubuntu() is False


def test_check_if_debian_or_ubuntu_handles_os_error():
    with patch(
        "preinstall.check_if_debian_or_ubuntu.platform.freedesktop_os_release",
        side_effect=OSError
    ):
        assert check_if_debian_or_ubuntu() is False