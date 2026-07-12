from GER.CORE.ger_banner import show_banner
from GER.CORE.ger_environment import validate_environment
from GER.CORE.ger_repository import validate_repository
from GER.CORE.bootstrap import initialize


def main():

    show_banner()

    validate_environment()

    validate_repository()

    initialize()

    print("\nGER FRAMEWORK READY")


if __name__ == "__main__":
    main()
