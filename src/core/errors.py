"""Handles errors associated with CLI functionality and inputs."""

class CLIBaseError(Exception):
    """The basic error class that more specific errors may inherit from."""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"message: {self.message}"

    def __repr__(self):
        return str(self)

class InvalidCategoryError(CLIBaseError):
    """Deals with incorrect categories being input to the CLI."""
    pass

class InvalidCommandError(CLIBaseError):
    """Deals with incorrect commands being input to the CLI."""
    pass
        