import os

from core.BaseController import BaseController
from utils.Prompt import prompt
from utils.ConfigManager import config_manager
from core.enums import OutputEnum


class Set(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    def outputType(self):
        config = config_manager.load()
        config["output_type"] = prompt.select("Set output type", [enum.value for enum in OutputEnum])
        config_manager.write(config)

        self.logger.complete(f"Output type set to '{config['output_type']}'")
        
        if config["output_type"] in [OutputEnum.File.value, OutputEnum.JSONFile.value]:
            self.outputDir()

    def outputDir(self):
        config = config_manager.load()
        output_dir = prompt.text(
            "Choose a directory for output files",
            required=True,
            default=config.get("output_dir", None)
        )
        config["output_dir"] = os.path.expanduser(output_dir)
        config_manager.write(config)

        self.logger.complete(f"Output directoy set to '{config['output_dir']}'")