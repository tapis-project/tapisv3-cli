import subprocess, os

from core.BaseController import BaseController
from utils.Prompt import prompt
from conf.settings import TMP_DIR, SOURCE_CODE_URL


class Update(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    def patch(self):
        if not self._has_deps():
            return
            
        self._update(scope="patch")

    def patch_and_install_dependencies(self):
        if not self._has_deps():
            return
            
        self._update(scope="update")

    def _has_deps(self):
        # Check that the required dependencies are install on the machine
        dependencies = ["git", "rsync"]
        self.logger.log("Checking dependencies...")
        found_dependencies = []
        for dependency in dependencies:
            proc = subprocess.run(f"{dependency} --version", shell=True, capture_output=True)
            if proc.returncode > 0:
                self.logger.error(f"Failed to update. Missing dependency '{dependency}'")
                return False

            found_dependencies.append(dependency)

        self.logger.complete(f"Found dependencies: {found_dependencies}")

        return True

    def _update(self, scope="patch"):
        scopes = ["patch", "update"]
        if scope not in scopes:
            raise Exception(f"Scope of update must be one of: {scopes}")

        # Build the commands that perform the update
        os.makedirs(TMP_DIR, exist_ok=True)
        cmd = f"cd {TMP_DIR} && git clone {SOURCE_CODE_URL} . && ./install {scope} && cd ../ && rm -rf {TMP_DIR}"
        subprocess.run(cmd, shell=True)

        self.logger.complete("TapisV3 CLI successfully updated")
        self.logger.warn("If you are using a tapis shell, please exit and restart a new shell for the changes to take effect")