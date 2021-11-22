import os

ACTION_FILTER_SUFFIX = "_Action"

PACKAGES = [
    "tapis",
    "tapipy",
    "jupyterscinco"
]

DEFAULT_PACKAGE = "core"

PACKAGES_DIR = "packages/"

AUTH_METHOD = "PASSWORD"

AUTH_METHODS = [ "PASSWORD" ]

# The user's username and password will be saved in the file below.
CONFIG_FILE = f"{os.path.expanduser('~')}/.tapisv3-cli/conf/configs.ini"
DEFAULT_CONFIG_FILE = CONFIG_FILE

PASSWORD = "PASSWORD"
DEFAULT_AUTH_METHOD = PASSWORD

