from dotenv import load_dotenv
from stages import setup_ssh_stage

def main():
    load_dotenv(".env")
    setup_ssh_stage.run()

if __name__ == "__main__":
    main()