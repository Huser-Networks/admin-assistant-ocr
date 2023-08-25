import json


class ConfigController:
    @staticmethod
    def load_config():
        with open('src/config/config.json', 'r') as file:
            return json.load(file)
