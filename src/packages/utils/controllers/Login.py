from tapipy.tapis import Tapis

from core.BaseController import BaseController
from utils.Prompt import prompt
from utils.Styles import styler as s
from utils.ConfigManager import config_manager

class Login(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    def index(self):
        base_url = prompt.text("Tapis baseurl")
        username = prompt.text("Username")
        password = prompt.text("Password 🔒", secret=True)

        self.logger.log(f"Authenticating with Tapis at {base_url} for user {username}")

        try:
            t = Tapis(
                base_url=base_url,
                username=username,
                password=password
            )
            t.get_tokens()
        except Exception as e:
            self.logger.error(f"Failed to authenticate: {e}")
            return

        self.logger.log("Successfully authenticated")
        
        jwt = t.get_access_jwt()
        
        # Update the users profile in the config or create a new one
        profile = config_manager.get_profile(username)
        if profile == None:
            profile = {"username": username, "base_url": base_url, "jwt": jwt}
            config_manager.create_profile(**profile)
            config_manager.set_current_user(username)
            self.logger.log(f"Created profile for user {username}")
            return

        config_manager.set_current_user(username)
        config_manager.update_profile(username, base_url=base_url, jwt=jwt)


    
