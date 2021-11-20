class Styles:
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

class Styler:
    def underline(self, string):
        return Styles.UNDERLINE + string + Styles.RESET

    def bold(self, string):
        return Styles.BOLD + string + Styles.RESET

styler = Styler()