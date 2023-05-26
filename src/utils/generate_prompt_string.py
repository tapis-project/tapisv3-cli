from utils.ConfigManager import config_manager


def generate_prompt_string():
    login_info = config_manager.get_current_login(config_manager.get_current_user())
    if login_info == None:
        return "[no user]"

    return f'{login_info["username"]}@{login_info["base_url"]}'.replace("https://", "")