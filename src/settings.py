from configparser import ConfigParser


# noinspection PyTypeChecker
class Settings:
    """
    Settings manager.
    """
    def __init__(self):
        self.config = ConfigParser()

    def initialize(self):
        self.config["settings"] = {
            "language":"English",
            "path":".\\data.db"
        }
        with open("../config.ini", "w") as configfile:
            self.config.write(configfile)

    def read_settings(self):
        self.config.read("config.ini")
        return [self.config.items(s) for s in self.config.sections()][0]

    def read_one_setting(self, setting):
        self.config.read("config.ini")
        return self.config.get('settings', setting)

    def set_settings(self, setting: str, value: str):
        self.config.read("config.ini")
        self.config.set("settings", setting, value)
        with open('.\\config.ini', 'w') as configfile:
            self.config.write(configfile)
