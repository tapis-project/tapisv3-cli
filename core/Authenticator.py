from tapipy.tapis import Tapis
from core.Logger import Logger
from typing import Union
import sys

class Authenticator:
    tenant = ""
    # @TODO add support for other authentication methods
    auth_methods = ["PASSWORD"]

    def __init__(self, tenant="https://tacc.develop.tapis.io"):
        self.tenant = tenant
        self.logger = Logger()

    def authenticate(self,
        credentials: dict, auth_method: str = "PASSWORD"
    ) -> Union[Tapis, None]:

        # Authenticate using the provided auth method. Raise exception
        # if provided credentials do not meet requirements
        if auth_method == "PASSWORD":
            self.validate_credentials(auth_method, credentials)
            try:
                client = Tapis(
                    base_url= self.tenant,
                    username=credentials["username"],
                    password=credentials["password"]
                )
                client.get_tokens()

                return client
            except:
                e = sys.exec_info[0]
                self.logger.log(e.message)
        else:
            return None

    def validate_credentials(self,
        auth_method: str, credentials: dict
    ) -> None:

        if auth_method == "PASSWORD":
            if not self.keys_in_dict(["username", "password"], credentials):
                raise ValueError("Provided credentials must contain a 'username' and 'password'")

    def keys_in_dict(self, keys: list, dict: dict) -> bool:
        for key in keys:
            if key not in dict:
                return False

        return True