import json
import sys

from tapipy.errors import InvalidInputError, ServerDownError

from packages.tapisetl.ETLController import ETLController


class Pipeline(ETLController):
    """Contains all of the CRUD functions associated with applications."""
    def __init__(self):
        ETLController.__init__(self)

    def create_Action(self, app_definition_file) -> None:
        pass
