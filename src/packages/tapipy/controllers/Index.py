from packages.tapipy.controllers.TapipyController import TapipyController
from utils.Prompt import prompt


class Index(TapipyController):
    def __init__(self):
        TapipyController.__init__(self)

    def invoke(self, *_, **__):
        # Prompt the user to select resource to perform
        resource_name = prompt.select("Perform action", self.client.resource_dicts.keys(), sort=True)
        self.set_resource(resource_name)
        (cmd, kw_args, args) = self.index()

        self.set_operation(cmd)
        self.set_cmd_options([])
        self.set_kw_args(kw_args)

        TapipyController.invoke(self, args)