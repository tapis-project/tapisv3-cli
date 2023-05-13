from utils.ConfigManager import config_manager as config

CONFIG = f"config.{config.get('package.jupyterscinco', 'tenant')}.{config.get('package.jupyterscinco', 'instance')}.jhub"