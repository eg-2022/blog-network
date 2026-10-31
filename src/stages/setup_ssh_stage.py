import subprocess
from helpers import status

MAINTAINERS_GROUP = "maintainers"

def create_maintainers_group() -> None:
    print(status.info("Creating 'maintainers' group..."))
    try:
        subprocess.run(["sudo", "groupadd", MAINTAINERS_GROUP])
    except PermissionError:
        print(status.error("Not enough privileges to execute the command"))

def check_group_existence() -> None:
    print(status.stage(1,"Setting up SSH server"))
    
    try:
        print(status.info(f"Checking if '{MAINTAINERS_GROUP}' group exists..."))
        group_exists = subprocess.run(["getent", "group", MAINTAINERS_GROUP],
                                text=True,
                                shell=False,
                                capture_output=True)

        if group_exists.returncode == 0:
            print(status.info(f"Group '{MAINTAINERS_GROUP}' exists already. Skipping..."))
        elif group_exists.returncode == 2:
            create_maintainers_group()
        else:
            print(status.error(f"There was an unexpected error while checking group: {group_exists.stderr}"))
    
    except FileNotFoundError:
        print(status.error("'getent' command was not found."))

    except PermissionError:
        print(status.error("Permission denied while executing 'getent'."))

    except OSError as e:
        print(status.error(f"OS error while executing 'getent: {e}'"))

def run():
    check_group_existence()