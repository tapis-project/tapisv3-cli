def generate_prompt_string(login_info):
    if login_info == None:
        return "[no user]"

    return f'{login_info["username"]}@{login_info["base_url"]}'