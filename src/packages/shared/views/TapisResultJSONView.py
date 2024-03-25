import json

from core.AbstractView import AbstractView


class TapisResultJSONView(AbstractView):
    def __init__(self, data, logger=None):
        self.data = data
        self.logger = logger

    def render(self):
        if type(self.data) in [str, int, float]:
            print(self.data)
            return

        if type(self.data) == bytes:
            self.logger.warn("Result is of type 'bytes'. Cannot show result")
            return
        
        print(json.dumps(self.data, indent=2))
