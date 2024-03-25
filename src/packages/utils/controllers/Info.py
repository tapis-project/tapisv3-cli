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
                "current_base_url": profile["current_base_url"]
            }], 
            headers={"current_user": "current user", "current_package": "current package", "current_base_url": "current base url"}
        )
        self.view.render()