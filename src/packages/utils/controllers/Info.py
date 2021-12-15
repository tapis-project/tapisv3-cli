from core.BaseController import BaseController


class Info(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    def index(self):
        self.set_view("DictTable", {
            "Profile": self.config.get("current", "profile"),
            "Package": self.config.get("current", "package"),
            "Auth method": self.config.get("current", "auth_method")
        })
        self.view.render()