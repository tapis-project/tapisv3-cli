from utils.Prompt import prompt

def build_config(tenant, instance, config_type, group=None):
    config = f"config.{tenant}.{instance}.jhub"
    if config_type == "group" and group is not None:
        config = f"{group}.group." + config

    return config
