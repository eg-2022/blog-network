import grp
import os
import pwd
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

SCRIPT_DIR = Path(__file__).resolve().parent
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
        status.info("Copying files to /etc/sshd/sshd_config.d/")
        shutil.copytree(
            src=source_dir,
            dst=destination_dir,
            dirs_exist_ok=True
        )
    except shutil.Error as e:
        print(f"Copy completed with errors. Failed items:")
        for source, destination, message in e.args[0]:
            print(f"Source: {source}")
            print(f"Destination: {destination}")
            print(f"Reason: {message}\n")
    except FileExistsError:
        print(f"Error: The destination directory '{destination_dir}' already exists.")

    except FileNotFoundError:
        print(f"Error: The source directory '{source_dir}' could not be found.")

    except PermissionError:
        print("Error: Access denied. Check your read/write permissions.")

    except OSError as e:
        print(f"System error occurred: {e}")

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

    sshd_config_files_dir = SCRIPT_DIR / "setup_ssh_stage.d" / "sshd_config.d"
    copy_sshd_config_files(str(sshd_config_files_dir), "/etc/ssh/sshd_config.d")
