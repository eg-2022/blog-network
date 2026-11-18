import os
from helpers import status

def check_if_root():
    if os.getuid() != 0:
        print(status.error("Please, run this program as root."))
        return False

    return True

def run():
    return check_if_root()