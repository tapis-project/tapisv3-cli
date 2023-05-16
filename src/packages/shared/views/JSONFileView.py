import os, json

from time import time

from core.AbstractView import AbstractView


class JSONFileView(AbstractView):
    def __init__(self, data, output_dir, filename_prefix="", logger=None):
        self.data = data
        self.output_dir = output_dir
        self.logger = logger
        self.filename_prefix = filename_prefix

    def render(self) -> None:
        os.makedirs(self.output_dir, exist_ok=True)
        filename_prefix = self.filename_prefix if self.filename_prefix == "" else "." + self.filename_prefix
        path_to_file = os.path.join(self.output_dir, str(time()).replace(".", "") + filename_prefix + ".json")

        with open(path_to_file, "w") as file:
            try:
                file.write(json.dumps(self.data, indent=2))
            except Exception as e:
                self.logger.error(f"JSON Error: {e}")

            if self.logger != None:
                self.logger.complete(f"Results saved to file: {path_to_file}")
