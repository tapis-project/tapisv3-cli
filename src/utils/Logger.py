from utils.Styles import Styles

class Logger:
    """Handles the error/success/info logging and sets their printed styles."""
    def complete(self, message):
        """Typically used for signifying that a task is done."""
        print(f"{Styles.SUCCESS}{Styles.BOLD}✓{Styles.RESET} {message}")

    def failed(self, message):
        """Used when an action cannot be successfully completed."""
        print(f"{Styles.ERROR}{Styles.BOLD}x{Styles.RESET} {message}")

    def success(self, message):
        """Used when an action is successfully completed."""
        print(f"\n{Styles.SUCCESS}Success:{Styles.RESET} {message}")

    def log(self, message=""):
        """Typically used to print a general message."""
        print(message)

    def newline(self, num_newlines):
        """Used to create space around command outputs on the CLI."""
        for i in range(num_newlines):
            print()

    def info(self, message=""):
        """Typically displayed when statuses change."""
        print(f"\n{Styles.INFO}Info:{Styles.RESET} {message}")

    def warn(self, message=""):
        """Used to warn the user of a potential error."""
        print(f"{Styles.WARNING}Warning:{Styles.RESET} {message}")

    def error(self, message=""):
        """Displays the error message when an error is thrown."""
        print(f"\n{Styles.ERROR}Error:{Styles.RESET} {message}")

    def debug(self, message=""):
        """Used to show the debug ouput. Not implemented as of yet."""
        print(f"{Styles.DEBUG}########## DEBUG ##########{Styles.RESET}\n{message}\n{Styles.DEBUG}######## END DEBUG ########{Styles.RESET}")
