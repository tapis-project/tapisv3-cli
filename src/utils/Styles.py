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
    MUTED = '\033[90m'

class Styler:
    def apply(self, style, string):
        return style + string + Styles.RESET

    def underline(self, string):
        return self.apply(Styles.UNDERLINE, string)

    def bold(self, string):
        return self.apply(Styles.BOLD, string)

    def muted(self, string):
        return self.apply(Styles.MUTED, string)

    def danger(self, string):
        return self.apply(Styles.ERROR, string)

    def blue(self, string):
        return self.apply(Styles.BLUE, string)

    

styler = Styler()