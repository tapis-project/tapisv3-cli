import os

ACTION_FILTER_SUFFIX = "_Action"

PACKAGES = ["tapis", "tapiscustom", "tapisetl"]

DEFAULT_PACKAGE = "tapis"

PACKAGES_DIR = "packages/"

TEMPLATES_DIR = "conf/templates/"

DEFAULT_AUTH_METHOD = "PASSWORD"

AUTH_METHODS = [ "PASSWORD" ]


PASSWORD = "PASSWORD"
DEFAULT_AUTH_METHOD = PASSWORD

LOG_LEVEL_DEFAULT = 1
LOG_LEVEL_VERBOSE = 2
LOG_LEVEL_DEBUG = 3

LOG_LEVEL = LOG_LEVEL_DEBUG

BASE_PATH = os.path.join(
    os.path.expanduser("~"),
    "tapis/v3"
)

TMP_DIR = os.path.join(BASE_PATH, "tmp")
CONFIG_DIR = os.path.join(BASE_PATH, "configs")

CONFIG_FILENAME = "config.json"

CONFIG_FILE_PATH = os.path.join(CONFIG_DIR, CONFIG_FILENAME)

SOURCE_CODE_URL = "https://github.com/tapis-project/tapisv3-cli.git"

