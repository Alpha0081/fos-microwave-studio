import json
from platform import system
from locale import getdefaultlocale


class Config:
    def __init__(self):
        with open("config.json", "r") as data:
            data = json.load(data)
            self.language = data["language"]
            self.language_default = getdefaultlocale()[0]
            self.system = system()
            self.font = data["font"]

    def reload(self):
        pass
    def save(self):
        pass

config = Config()