import os

from core.BaseController import BaseController
from utils.Prompt import prompt
from utils.ConfigManager import config_manager
from core.enums import OutputEnum


class Set(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    def username(self):
        # Prompt for the new username
        current_user = config_manager.get_current_user()
        new_username = prompt.text("New username", default=current_user, required=True)
        
        # Create the modified profile
        current_profile = config_manager.get_profile(current_user)
        modified_profile = {**current_profile, "username": new_username}

        # Update the current user
        config_manager.set_current_user(new_username)

        # Update the profile list with the new profile
        modified_profiles = []
        config = config_manager.load()
        for profile in config.get("profiles"):
            # Add only non-current user profiles to the list
            if profile["username"] != current_user:
                modified_profiles.append(profile)

        # Add the newly modified profile to the profiles list
        modified_profiles.append(modified_profile)
        config["profiles"] = modified_profiles
        
        config_manager.write(config)

        self.logger.complete(f"Username updated from '{current_user}' to '{new_username}'")

    def jwt(self):
        current_user = config_manager.get_current_user()
        jwt = prompt.text("New JWT", required=True)

        config_manager.update_profile(current_user, jwt=jwt)

        self.logger.complete(f"JWT updated")
        

    def output_type(self):
        config = config_manager.load()
        config["output"]["type"] = prompt.select(
            "Set output type",
            [enum.value for enum in OutputEnum]
        )
        config_manager.write(config)

        self.logger.complete(f"Output type set to '{config['output']['type']}'")
        
        if config['output']['type'] in [OutputEnum.File.value, OutputEnum.JSONFile.value]:
            self.output_dir()

    def output_dir(self):
        config = config_manager.load()
        output_dir = prompt.text(
            "Choose a directory for output files",
            required=True,
            default=config.get("output").get("dir", None)
        )
        config["output"]["dir"] = os.path.expanduser(output_dir)
        config_manager.write(config)

        self.logger.complete(f"Output directoy set to '{config['output']['dir']}'")

    def display_settings(self):
        config = config_manager.load()

        max_columns = prompt.text(
            "Maximum # of columns to display in table view (int)",
            default=config.get("output").get("settings").get("max_columns"),
            value_type=int
        )

        max_chars_per_column = prompt.text(
            "Maximum # of characters per column (int)",
            default=config.get("output").get("settings").get("max_chars_per_column"),
            value_type=int
        )

        default_never_truncate = ",".join(config.get("output").get("settings").get("never_truncate"))
        never_truncate = prompt.text(
            "List of properties exempt from trunction (comma-seperated list of strings)",
            default=default_never_truncate,
        )
        never_truncate = never_truncate.replace(" ", "").split(",")

        first_column = prompt.text(
            "Column name to show first tables: Ex: 'id', 'uuid', 'jobUuid'",
            default=config.get("output").get("settings").get("first_column"),
            value_type=str
        )

        config["output"]["settings"] = {
            "max_columns": max_columns,
            "max_chars_per_column": max_chars_per_column,
            "never_truncate": never_truncate,
            "first_column": first_column
        }

        config_manager.write(config)

        self.logger.complete(f"Display settings updated")