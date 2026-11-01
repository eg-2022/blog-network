import grp
import os
import pwd
import requests
import shutil
import subprocess
from pathlib import Path

from helpers import status

def get_current_user() -> str:
    username = os.environ.get("SUDO_USER")

    if username is None:
        username = pwd.getpwuid(os.getuid()).pw_name

    try:
        pwd.getpwnam(username)
    except KeyError:
        raise RuntimeError(f"User '{username}' does not exist")

    return username

SETUP__SSH_STAGE_D = Path(__file__).resolve().parent / "setup_ssh_stage.d"
MAINTAINERS_GROUP = "maintainers"
CURRENT_USER = get_current_user()

def is_running_as_root() -> bool:
    return os.getuid() == 0

def create_maintainers_group() -> None:
    print(status.info("Creating 'maintainers' group..."))
    try:
        result = subprocess.run(["groupadd", MAINTAINERS_GROUP],
                                text=True,
                                capture_output=True)

        if result.returncode == 0:
            print(status.success(f"Group: '{MAINTAINERS_GROUP}' created successfully."))
        else:
            print(status.error(result.stderr.strip()))


    except OSError as e:
        print(status.error(f"OS error while executing 'groupadd': {e}").strip())

def check_group_existence() -> bool:
    try:
        print(status.info(f"Checking if '{MAINTAINERS_GROUP}' group exists..."))
        result = subprocess.run(["getent", "group", MAINTAINERS_GROUP],
                                text=True,
                                capture_output=True)

        if result.returncode == 0:
            print(status.info(f"Group '{MAINTAINERS_GROUP}' exists already. Skipping..."))
            return True
        
        if result.returncode == 2:
            create_maintainers_group()

            return subprocess.run(
                ["getent", "group", MAINTAINERS_GROUP],
                capture_output=True,
                text=True
            ).returncode == 0

        print(status.error(result.stderr.strip()))
        return False
    
    except FileNotFoundError:
        print(status.error("'getent' command was not found."))
        return False

    except OSError as e:
        print(status.error(f"OS error while executing 'getent': {e}").strip())
        return False

def add_user_to_group(user: str, group: str) -> None:
    try:
        print(status.info(f"Adding user: '{user}' to group: '{group}'."))
        result = subprocess.run(["usermod", "-aG", group, user],
                                text=True,
                                capture_output=True)

        if result.returncode == 0:
            print(status.success(f"User: '{user}' added to group: '{group}'"))
        else:
            print(status.error(result.stderr.strip()))

    except OSError as e:
            print(status.error(f"OS error while executing 'usermod': {e}").strip())

def check_if_user_belongs_to_group() -> bool:
    try:
        group = grp.getgrnam(MAINTAINERS_GROUP)
        user = pwd.getpwnam(CURRENT_USER)

        return (
            user.pw_gid == group.gr_gid
            or CURRENT_USER in group.gr_mem
        )
    except KeyError:
        return False

def copy_sshd_config_files(source_dir: str, destination_dir: str) -> None:
    try:
        print(status.info("Copying files to /etc/sshd/sshd_config.d/"))
        shutil.copytree(
            src=source_dir,
            dst=destination_dir,
            dirs_exist_ok=True
        )
        print(status.success("Copied files to /etc/sshd_config.d/ succesfully"))

    except shutil.Error as e:
        print(status.error(f"Copy completed with errors. Failed items:"))
        for source, destination, message in e.args[0]:
            print(f"Source: {source}")
            print(f"Destination: {destination}")
            print(f"Reason: {message}\n")

    except FileNotFoundError:
        print(status.error(f"Error: The source directory '{source_dir}' could not be found."))

    except PermissionError:
        print(status.error("Error: Access denied. Check your read/write permissions."))

    except OSError as e:
        print(status.error(f"System error occurred: {e}"))

def download_public_keys_for_ssh():
    url = os.getenv("GITHUB_SSH_KEY")
    destination = Path.home() / ".ssh" / "authorized_keys"
    user_id = pwd.getpwuid(os.getuid()).pw_uid
    group_id = pwd.getpwuid(os.getgid()).pw_gid

    print(status.info("Downloading public key(s)..."))

    if url:
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        destination.parent.mkdir(parents=True, exist_ok=True)

        with destination.open("ab") as file:
            file.write(response.content)

        destination.chmod(0o600)

        os.chown(destination, user_id, group_id)

def run():
    if not is_running_as_root():
        print(status.error(
            "This script must be executed with sudo."
        ))
        return

    print(status.stage(1,"Setting up SSH server"))
    print(status.info(f"Configuring system for user: '{CURRENT_USER}'"))

    if not check_group_existence():
        print(status.error(
            "Unable to create or verify maintainers group."
        ))
        return

    if not check_if_user_belongs_to_group():
        add_user_to_group(CURRENT_USER, MAINTAINERS_GROUP)
    else:
        print(status.info(f"'{CURRENT_USER}' already belongs to group: '{MAINTAINERS_GROUP}'. Skipping..."))

    sshd_config_files_dir = SETUP__SSH_STAGE_D / "sshd_config.d"
    copy_sshd_config_files(str(sshd_config_files_dir), "/etc/ssh/sshd_config.d")

    download_public_keys_for_ssh()