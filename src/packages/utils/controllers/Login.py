# NOTE FIXME This belongs in the tapis package

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
            current_base_url = profile.get("current_base_url", None)
        
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

        self.logger.complete("Successfully authenticated")
        
        jwt = t.get_access_jwt()
        
        # Update the users profile in the config or create a new one
        profile = config_manager.get_profile(username)
        if profile == None:
            config_manager.create_profile({
                "username": username,
                "current_base_url": base_url,
                "auths": [
                    {
                        "base_url": base_url,
                        "jwt": jwt
                    }
                ],
            })
            config_manager.set_current_user(username)
            self.logger.complete(f"Created profile for user {username}")
            return

        config_manager.set_current_user(username)
        modified_auths = [
            auth for auth in profile["auths"]
            if auth["base_url"] != base_url
        ]
        modified_auths.append({"base_url": base_url, "jwt": jwt})
        config_manager.update_profile({
            "username": username,
            "current_base_url": base_url,
            "auths": modified_auths
        })


    
