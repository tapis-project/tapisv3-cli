from core.BaseController import BaseController


class Set(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    def tenant(self, tenant):
        self.set_config("tenant", tenant)

    def instance(self, instance):
        self.set_config("instance", instance)

    def database(self, database):
        self.set_config("database", database)

    def collection(self, collection):
        self.set_config("collection", collection)