def cmd_to_class(cmd: str) -> str:
    class_name = ""
    modified_cmd = cmd.replace("_", "-")
    parts = modified_cmd.split("-")
    for part in parts:
        class_name += "".join(part.capitalize())

    return class_name
