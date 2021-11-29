from utils.ConfigManager import ConfigManager

conf = ConfigManager()

ENVS = [ "develop", "staging", "prod" ]

# Default to prod env
ENV = conf.get("tapis", "env") if conf.has_key("tapis", "env") else "prod"
if ENV not in ENVS:
    raise Exception(f"Configuration Error: '{ENV}' is not a valid ENV. Valid Envs: {ENVS}")

# Default to tacc tenant
TENANT = conf.get("package.tapis", "tenant") if conf.has_key("package.tapis", "env") else "tacc"

# Build the base url for tapis queries
_env_str = ENV + "." if (ENV != "prod") else ""
BASE_URL = f"https://{TENANT}.{_env_str}tapis.io"