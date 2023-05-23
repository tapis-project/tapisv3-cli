import os

from core.BaseController import BaseController
from utils.Prompt import prompt
from utils.ConfigManager import config_manager
from core.enums import OutputEnum
from packages.utils.controllers.Display import Display
from packages.utils.controllers.Output import Output


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
        

    def output_settings(self):
        output_controller = Output()
        output_controller.index()

    def display_settings(self):
        display_controller = Display()
        display_controller.settings()