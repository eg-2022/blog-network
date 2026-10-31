import subprocess
from helpers import status

def main():
    print(status.stage(1,"Setting up SSH server"))

    # Task 1: Maintainers group existence
    try:
        print(status.info("Checking if 'maintainers' group exists..."))
        group_exists = subprocess.run(["getent", "group", "maintainers"],
                                text=True,
                                shell=False,
                                capture_output=True)

        if group_exists.returncode == 0:
            print(status.info("Group 'maintainers' exists already."))
        elif group_exists.returncode == 2:
            print(status.info("Creating group 'maintainers'."))
        else:
            print(status.error(f"There was an unexpected error while checking group: {group_exists.stderr}"))
    
    except FileNotFoundError:
        print(status.error("'getent' command was not found."))

    except PermissionError:
        print(status.error("Permission denied while executing 'getent'."))

    except OSError as e:
        print(status.error(f"OS error while executing 'getent: {e}'"))

    finally:
        print(status.success("Script has finished"))

if __name__ == "__main__":
    main()