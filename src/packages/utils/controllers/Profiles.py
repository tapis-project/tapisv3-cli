from core.BaseController import BaseController
from utils.Prompt import prompt
from utils.Styles import styler as s


class Profiles(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    def index(self):
        self.list()

    def use(self):
        current_user = self.config_manager.get_current_user()
        profiles = self.config_manager.list_profiles()
        if len(profiles) == 0:
            self.logger.warn("No profiles to choose from. Run `tapis login` to create a profile")
            return
        
        usernames = [profile["username"] for profile in profiles]

        current_user_str = s.muted(f"[{current_user}]")
        new_current_user = prompt.select(
            f"Choose a profile: {current_user_str}",
            [username for username in usernames]
        )
        
        self.config_manager.set_current_user(new_current_user)

        self.logger.complete(f"Using profile for user '{new_current_user}'")

    def remove(self):
        profiles = self.config_manager.list_profiles()
        if len(profiles) == 0:
            self.logger.log("No profiles to remove")
            return

        username = prompt.select(f"Choose profile to remove", [profile["username"] for profile in profiles])
        confirmed = prompt.confirm(f"Are you sure you want to delete {username}?")
        
        if confirmed:
            self.config_manager.delete_profile(username)
            self.logger.log(f"Profile for {username} deleted")
            self.exit(1)

        self.logger.log("Action cancelled. Profile not deleted")
        self.exit(1)

    def list(self):
        # Fetch the profiles from the config
        profiles = self.config_manager.list_profiles()
        if len(profiles) == 0:
            self.logger.info("No profiles found")
            return

        self.set_view("DictTable", [
                {
                    **profile,
                    "jwt": "..." + profile["jwt"][-16:]
                } for profile in profiles
            ],
            headers={"username": "username", "base_url": "base_url", "jwt": "jwt"}
        )

        self.view.render()

    
