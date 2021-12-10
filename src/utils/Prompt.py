import sys
import inquirer
from inquirer.themes import Default
from getpass import getpass
from utils.Styles import styler as s
from typing import List

class Prompt:
    def __init__(self):
        self.no_vals = ["N", "n", "no", "No", "NO"]
        self.yes_vals = ["Y", "y", "yes", "Yes", "YES"]
        self.theme = Default()

    # TODO provide tab functionality to tab through dirs on users machine
    def text(self,
        message: str,
        secret: bool = False,
        default: any = None, # TODO limit types (no objects, dicts, arrays, etc)
        nullable: bool = False,
        description: str = None,
        value_type: callable = None
    ) -> str:
        """
        Prompts the user for input described in the message. If secret is set
        to true, user input is not shown. If the user doesn't put any input,
        warn them that they must input a value and call this function recursively.
        """
        # If secret set to False, allow user input to be visible and return it
        # If secret set to True, do not allow user input to be visible and return it
        prompt = input
        if secret:
            prompt = getpass

        modified_message = message

        # Add description to message
        if description is not None:
            modified_message = modified_message + s.muted(f" {description}")

        # Add default value to message
        if default is not None:
            modified_message = modified_message + s.muted(f" [{default}]")

        modified_message = modified_message + ": "

        # Prompt user for input
        value = prompt(modified_message)

        # If no value is provided, set the value to the default value
        if bool(value) == False and default is not None:
            value = default

        # Reprompt if not nullable and user provides null value
        if nullable is False and bool(value) == False:
            print("You must provide a value.")
            return self.text(
                message,
                secret=secret,
                default=default,
                nullable=nullable,
                description=description,
                value_type=value_type
            )

        # Reprompt user if they provide a value of the incorrect type
        if value_type is not None and self._validate_type(value_type, value) == False:
            print("Incorrect type provided")
            return self.text(
                message,
                secret=secret,
                default=default,
                nullable=nullable,
                description=description,
                value_type=value_type
            )

        return value

    def yes_no(self, message, exit=True) -> None:
        """
        Prompts the user for yes or no input. The script will exit if anything
        except for a 'yes' answer is selected.
        """
        yn = input(message)

        # If user selects 'no' then exit the script, if the user selects 'yes'
        # then pass to continue the script, otherwise exit the script if the
        # user doesn't provide any valid selections.
        if yn in self.no_vals:
            if exit == True:
                sys.exit(1)
            return False
        elif yn in self.yes_vals:
            return True
        else:
            print("Invalid option required. Must type 'y' for yes or 'n' for no.")
            sys.exit(1)

    # Recursively calls a callback until the value provided by a user matches
    # the permitted values
    def validate_choices(self, message, choices: list, callback: callable):
        value = callback(message)
        if value not in choices:
            print(f"Invalid value '{value}': Choose one of the permitted values: {choices}")
            return callback(message)

        return value

    def confirm(self, message):
        questions = [
            inquirer.List("choice",
                message=message,
                choices=["confirm", "cancel"]
            ),
        ]

        answer = inquirer.prompt(questions, theme=self.theme)["choice"]

        if answer == "confirm":
            return True
        
        return False


    def select(self,
        message,
        choices: List[str],
        description: str = None,
        carousel=True,
        cancel=False,
        sort=False
    ):
        # Add cancel as an option if cancel == True
        # Non-printable character used to prevent users from providing a choice
        # that would cancel
        np = "\t"
        cancel_string = s.muted(f"[x] cancel{np}")
        if cancel:
            choices.append(cancel_string)
        
        if sort:
            choices = sorted(choices)

        # Add description to message
        if description is not None:
            message = message + s.muted(f" {description}")

        questions = [
            inquirer.List('choice',
                message=message,
                choices=choices,
                carousel=carousel
            ),
        ]

        answer = inquirer.prompt(questions, theme=self.theme)["choice"]
        if answer == cancel_string:
            sys.exit(1)

        return answer

    def select_bool(self, message, description=None, carousel=True):
        if description is not None:
            message = message + s.muted(f" {description}")

        questions = [
            inquirer.List("choice",
                message=message,
                choices=[True, False],
                carousel=carousel
            ),
        ]
        
        return inquirer.prompt(questions, theme=self.theme)["choice"]

    def checkbox(self, message, choices):
        message = message + s.muted(" Space to select. Enter to confirm")
        questions = [ 
            inquirer.Checkbox("choice",
                message=message,
                choices=choices
            ) 
        ]

        return inquirer.prompt(questions, theme=self.theme)["choice"]

    def editor(self, message, description: str = None):
        modified_message = message

        # Add description to message
        if description is not None:
            modified_message = modified_message + s.muted(f" {description}")

        questions = [
            inquirer.Editor('text', message=modified_message)
        ]
        return inquirer.prompt(questions, theme=self.theme)["text"]

    def _validate_type(self, type_fn, value):
        try:
            type_fn(value)
            return True
        except:
            return False

prompt = Prompt()