from tapipy.tapis import Tapis

from core.BaseController import BaseController
from utils.Prompt import prompt
from utils.ConfigManager import config_manager

class Login(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    def index(self):
        current_user = config_manager.get_current_user()
        profile = config_manager.get_profile(current_user)
        current_base_url = None
        if profile != None:
            current_base_url = profile.get("base_url", None)
        
        base_url = prompt.text("Tapis baseurl", default=current_base_url)
        username = prompt.text("Username", default=current_user)
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


    
