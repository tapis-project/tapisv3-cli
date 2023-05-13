from core.BaseController import BaseController


class Info(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    def index(self):
        current_user = self.config_manager.get_current_user()
        current_package = self.config_manager.get_current_package()
        profile = self.config_manager.get_profile(current_user)
        self.set_view("DictTable", [{
                "current_user": current_user,
                "current_package": current_package,
                "base_url": profile["base_url"],
                "jwt": "..." + profile["jwt"][-16:]
            }], 
            headers={"current_user": "current_user", "current_package": "current_package", "base_url": "base_url", "jwt": "jwt"}
        )
        self.view.render()