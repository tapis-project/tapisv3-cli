""" 
All settings and configurable variables, such as environment varaibles, go here.

There are two tenants within TAPIS: tacc and dev
There are three environments: develop, staging, and prod

The appropriate environment should be substituted below based on the progress
of development for a feature or for testing purposes. For example:
    * tacc.develop.tapis.io = TACC tenant in development environment
    * dev.staging.tapis.io = DEV tenant in the staging environment

NOTE: The TACC tenant in production is tacc.tapis.io, not tacc.prod.tapis.io!
"""

APP_REGISTRY = [
    "core",
    "tapis"
]

AUTH_METHOD = "PASSWORD"

AUTH_METHODS = [ "PASSWORD" ]

# The user's username and password will be saved in the file below.
CONFIG_FILE = "configs/configs.ini"
DEFAULT_CONFIG_FILE = CONFIG_FILE

PASSWORD = "PASSWORD"
DEFAULT_AUTH_METHOD = PASSWORD

# See docstring for info on the below.
ENVS = [ "develop", "staging", "prod" ]

ENV = "prod"
TENANT = "tacc"

ENV = ENV + "." if (ENV != "prod") else ""

BASE_URL = f"https://{TENANT}.{ENV}tapis.io"