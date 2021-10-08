import sys
from getpass import getpass

class Prompt:
    def not_none(self, message: str, secret: bool = False) -> str:
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

        value = prompt(message)

        if value == None:
            print("You cannot provide and empty value.\n")
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
        if yn == "n" or yn == "N":
            sys.exit(1)
        elif yn == "y" or yn == "Y":
            return
        else:
            print("Invalid option required. Must type 'y' for yes or 'n' for no.\n")
            sys.exit(1)

prompt = Prompt()