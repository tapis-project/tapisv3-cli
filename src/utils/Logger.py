"""Handles the error/success/info logging and sets their printed styles."""

class styles:
    """The colors associated with the logging messages."""
    DEBUG = '\033[95m'
    BLUE = '\033[94m'
    SUCCESS = '\033[92m'
    INFO = '\033[96m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Logger:
    """Contains the various log categories and their printed messages."""
    def complete(self, message):
        # Typically used for signifying that a task is done.
        print(f"{styles.SUCCESS}{styles.BOLD}✓{styles.RESET} {message}")

    def failed(self, message):
        # Used when an action cannot be successfully completed.
        print(f"{styles.ERROR}{styles.BOLD}x{styles.RESET} {message}")

    def success(self, message):
        # Used when an action is successfully completed.
        print(f"\n{styles.SUCCESS}Success:{styles.RESET} {message}")

    def log(self, message=""):
        # Typically used to print a general message.
        print(message)

    def newline(self, num_newlines):
        # Used to create space around command outputs on the CLI.
        for i in range(num_newlines):
            print()

    def info(self, message=""):
        # Typically displayed when statuses change.
        print(f"\n{styles.INFO}Info:{styles.RESET} {message}")

    def warn(self, message=""):
        # Used to warn the user of a potential error.
        print(f"{styles.WARNING}Warning:{styles.RESET} {message}")

    def error(self, message=""):
        # Displays the error message when an error is thrown.
        print(f"\n{styles.ERROR}Error:{styles.RESET} {message}")

    def debug(self, message=""):
        # Used to show the debug ouput. Not implemented as of yet.
        print(f"{styles.DEBUG}########## DEBUG ##########{styles.RESET}\n{message}\n{styles.DEBUG}######## END DEBUG ########{styles.RESET}")
    
