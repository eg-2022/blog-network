import grp
import subprocess
from helpers import status

MAINTAINERS_GROUP = "maintainers"

def check_if_group_created():
    try:
        grp.getgrnam(MAINTAINERS_GROUP)
        print(status.info(f"Groups: {MAINTAINERS_GROUP} already exists."))
        return True
    except KeyError:
        pass

def create_maintainers_group():
    if check_if_group_created():
        return True

    try:
        subprocess.run(
            ["groupadd", MAINTAINERS_GROUP],
            check=True,
            text=True,
            capture_output=True
        )
        print(status.info(f"Group: {MAINTAINERS_GROUP} was defined."))
        return True

    except FileNotFoundError:
        print(status.error("The groupadd command was not found."))

    except PermissionError:
        print(status.error("Insufficient permissions to execute groupadd."))

    except subprocess.CalledProcessError as e:
        print(status.error(f"Could not create group: {e.stderr.strip()}"))

    except OSError as e:
        print(status.error(f"Operating system error: {e}"))

    return False

def run():
    return create_maintainers_group()