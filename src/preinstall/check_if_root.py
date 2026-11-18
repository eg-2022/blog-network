import os

def check_if_root():
    if os.getuid() != 0:
        print("[ERROR] Please, run this program as root.")
        return False

    return True

def run():
    return check_if_root()