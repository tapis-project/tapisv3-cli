import os

from core.BaseController import BaseController
from utils.Prompt import prompt
from utils.ConfigManager import config_manager
from core.enums import OutputEnum


class Output(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    def set_output_type(self):
        config = config_manager.load()
        config["output"]["type"] = prompt.select(
            "Set output type",
            [enum.value for enum in OutputEnum]
        )
        config_manager.write(config)

        self.logger.complete(f"Output type set to '{config['output']['type']}'")
        
        if config['output']['type'] in [OutputEnum.File.value, OutputEnum.JSONFile.value]:
            self.set_output_dir()

    def set_output_dir(self):
        config = config_manager.load()
        output_dir = prompt.text(
            "Choose a directory for output files",
            required=True,
            default=config.get("output").get("dir", None)
        )
        config["output"]["dir"] = os.path.expanduser(output_dir)
        config_manager.write(config)

        self.logger.complete(f"Output directoy set to '{config['output']['dir']}'")