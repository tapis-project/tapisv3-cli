from core.BaseController import BaseController


class Set(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    def index(self):
        method_names = self.get_methods()
        
        for method_name in method_names:
            method = getattr(self, method_name)
            (arg_vals, kwarg_vals) = self._prompt_arg_kwarg_vals(method)
            method(*arg_vals, **kwarg_vals)

    def tenant(self, tenant):
        self.set_config("tenant", tenant)

    def instance(self, instance):
        self.set_config("instance", instance)

    def database(self, database):
        self.set_config("database", database)

    def collection(self, collection):
        self.set_config("collection", collection)