import shutil
import sys
from pathlib import Path
from helpers import status

SOURCE = Path(__file__).parent / "files" / "sshd_config.d"
DESTINATION = Path("/etc/ssh/sshd_config.d")

def check_source_directory(source: Path):
    # Check if /etc/ssh/sshd_config.d exists
    if not Path.exists(source):
        print(status.error("Source directory not found. Installation could have gone wrong."))
        sys.exit(1)    
        return False
    
    return True

def check_destination_directory(destination: Path):
    # Check if /etc/ssh/sshd_config.d exists
    if not Path.exists(destination):
        print(status.error("Destination directory not found. Installation could have gone wrong."))
        sys.exit(1)    
        return False
    
    return True

def copy_directory_to_source(source: str, destination: str):
    # Copy files from SOURCE to DESTINATION
    try:
        print(status.info("Copying files to /etc/ssh/sshd_config.d/"))
        shutil.copytree(src=source,
                dst=destination,
                dirs_exist_ok=True)
        print(status.success("Files were copied successfully"))
        return True
    except FileNotFoundError as e:
        print(status.error(f"Directory couldn't be found: {e}"))
        return False
    except NotADirectoryError:
        print(status.error(f"File detected. Not a directory."))
        return False
    except PermissionError as e:
        print(status.error(f"There's a problem with system permissions: {e}"))
    except shutil.Error as e:
        print(status.error("An error has happened during copying process."))

def run():
    checks = (
        lambda: check_source_directory(SOURCE),
        lambda: check_destination_directory(DESTINATION),
    )

    for check in checks:
        if not check():
            return False

    if not copy_directory_to_source(SOURCE, DESTINATION):
        return False

    return True