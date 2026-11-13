import os
import sys

def main():
    if os.getuid() != 0:
        print("Please, run this program as root.")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())