from utils.Styles import styler as s

class HelpFormatter:
    usage_message: str
    commands_message: str
    options_message: str
    command: list
    options: list
    def __init__(self):
        self._set_initial_state()

    def add_usage(self, usage: str):
        self.usage_message = self.usage_message + usage

    def add_command(self,
        command_name,
        positional_args=[],
        optional_keyword_args=[],
        required_keyword_args=[]
    ):
        pos_args_msg = ""
        if len(positional_args) > 0:
            pos_args_msg = "\n    positional args: "
            pos_args_msg = pos_args_msg + f"[{', '.join([arg for arg in positional_args])}]"

        kw_args_msg = ""
        if len(required_keyword_args) > 0:
            kw_args_msg = "\n    required keyword args: "
            kw_args_msg = kw_args_msg + "[" + ", ".join([f"--{arg}" for arg in required_keyword_args]) + "]"

        if len(optional_keyword_args) > 0:
            kw_args_msg += "\n    optional keyword args: "
            kw_args_msg += "[" + ", ".join([f"--{arg}" for arg in optional_keyword_args]) + "]"
        
        self.commands_message = self.commands_message + (
            f"{s.underline(s.blue(command_name))}{pos_args_msg}{kw_args_msg}\n"
        )

    def add_options(self, options: list):
        for option in options:
            self.options_message = self.options_message + f"{option.name} [{''.join(option.aliases)}] | Description: {option.description}\n"

    def build(self):
        help_message = (
            "\n" + f"{self.usage_message}"
            "\n\n" + f"{self.commands_message}"
            # "\n\n" + f"{self.options_message}"
        )

        # NOTE Initial state needs to be reset on every call of 'build'
        # because the help formatter exists as a singleton and can be
        # used multiple times in a single shell session
        self._set_initial_state()

        return help_message

    def _set_initial_state(self):
        self.usage_message = f"{s.underline('Usage')}: "
        self.commands_message = f"{s.underline('Commands')}:\n"
        self.options_message = f"{s.underline('Options')}:\n"
        self.commands = []
        self.options = []

help_formatter = HelpFormatter()