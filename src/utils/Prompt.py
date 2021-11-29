import sys
import inquirer
from getpass import getpass
from utils.Styles import styler as s

class Prompt:
    def __init__(self):
        self.no_vals = ["N", "n", "no", "No", "NO"]
        self.yes_vals = ["Y", "y", "yes", "Yes", "YES"]

    def not_none(self,
        message: str,
        secret: bool = False,
        default: any = None # TODO limit types (no objects, dicts, arrays, etc)
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

        if default is not None:
            message = message + s.muted(f" [{default}]")

        modified_message = message + ": "

        value = prompt(modified_message)

        if bool(value) == False:
            print("You cannot provide and empty value.")
            return self.not_none(message, secret)

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

    def select(self, question, choices, carousel=True):
        questions = [
            inquirer.List('choice',
                message=question,
                choices=choices,
                carousel=carousel
            ),
        ]

        return inquirer.prompt(questions)["choice"]

    def select_cancel(self, question, choices, carousel=True):
        # Non-printable character used to prevent users from providing a choice
        # that would cancel
        np = "\t"
        cancel_string = s.danger(f"[x] cancel{np}")
        choices.append(cancel_string)
        answer = self.select(question, choices, carousel)

        if answer == cancel_string:
            sys.exit(1)
        
        return answer

prompt = Prompt()