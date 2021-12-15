from typing import Dict, Union, AnyStr

class SettingSet:
    def __init__(self, settings: Dict[str, Union[AnyStr, int]]):
        for key, value in settings.items():
            setattr(self, key, value)