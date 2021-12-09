import os
from re import VERBOSE

ACTION_FILTER_SUFFIX = "_Action"

PACKAGES = [
    "tapis",
    "tapipy",
    "jupyterscinco"
]

DEFAULT_PACKAGE = "tapipy"

PACKAGES_DIR = "packages/"

TEMPLATES_DIR = "conf/templates/"

DEFAULT_AUTH_METHOD = "PASSWORD"

AUTH_METHODS = [ "PASSWORD" ]

# The user's username and password will be saved in the file below.
CONFIG_FILE = f"{os.path.expanduser('~')}/.tapisv3-cli/conf/configs.ini"
DEFAULT_CONFIG_FILE = CONFIG_FILE

PASSWORD = "PASSWORD"
DEFAULT_AUTH_METHOD = PASSWORD

LOG_LEVEL_DEFAULT = 1
LOG_LEVEL_VERBOSE = 2
LOG_LEVEL_DEBUG = 3

LOG_LEVEL = LOG_LEVEL_DEBUG

