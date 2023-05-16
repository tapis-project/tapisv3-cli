import os, json

from time import time

from core.AbstractView import AbstractView


class FileView(AbstractView):
    def __init__(self, data, output_dir, filename_prefix="", logger=None):
        self.data = data
        self.output_dir = output_dir
        self.logger = logger
        self.filename_prefix = filename_prefix

    def render(self) -> None:
        os.makedirs(self.output_dir, exist_ok=True)
        filename_prefix = self.filename_prefix if self.filename_prefix == "" else "." + self.filename_prefix
        path_to_file = os.path.join(self.output_dir, str(time()).replace(".", "") + filename_prefix + ".txt")

        with open(path_to_file, "w") as file:
            file.write(str(self.data))
            if self.logger != None:
                self.logger.complete(f"Results saved to file: {path_to_file}")
