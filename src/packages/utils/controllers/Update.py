import subprocess, os

from core.BaseController import BaseController
from utils.Prompt import prompt
from conf.settings import TMP_DIR, SOURCE_CODE_URL


class Update(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    def index(self):
        # Check that the required dependencies are install on the machine
        dependencies = ["git", "rsync"]
        self.logger.log("Checking dependencies...")
        found_dependencies = []
        for dependency in dependencies:
            proc = subprocess.run(f"{dependency} --version", shell=True, capture_output=True)
            if proc.returncode > 0:
                self.logger.error(f"Failed to update. Missing dependency '{dependency}'")
                return

            found_dependencies.append(dependency)

        self.logger.complete(f"Found dependencies: {found_dependencies}")

        # Build the commands that perform the update
        os.makedirs(TMP_DIR, exist_ok=True)
        cmd = f"cd {TMP_DIR} && git clone {SOURCE_CODE_URL} . && ./install patch && cd ../ && rm -rf {TMP_DIR}"
        subprocess.run(cmd, shell=True)

        self.logger.complete("TapisV3 CLI successfully updated")
        self.logger.warn("If you are using a tapis shell, please exit and restart a new shell for the changes to take effect")

