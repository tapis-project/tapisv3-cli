from utils.ConfigManager import configManager as config

CONFIG = f"config.{config.get('package.jupyterscinco', 'tenant')}.{config.get('package.jupyterscinco', 'instance')}.jhub"