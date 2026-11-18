import os

def check_if_posix():
    if os.name != "posix":
        print(f"Not a valid operative system: {os.name}")
        return False

    return True

def run():
    return check_if_posix()