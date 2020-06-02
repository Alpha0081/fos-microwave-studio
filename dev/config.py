import json

class Config:
    def __init__(self):
        with open("config.json", "r") as data:
            data = json.load(data)
            self.language = data["language"]
    def reload(self):
        pass
    def save(self):
        pass
