import json

class SettingsManager():
    def __init__(self, settings_file):
        self.settings_file = settings_file
        self.settings = {}
        self.keybinds = {}

        with open(settings_file) as jsonfile:
            self.settings = json.load(jsonfile)
            self.keybinds = self.settings["keybinds"]
            

    def get_keybind(self, action):
        return self.keybinds[action]

    def set_keybind(self, action, key):
        self.settings["keybinds"][action] = key
        self.save_settings()

    def save_settings(self):
        with open(self.settings_file, 'w') as jsonfile:
            json.dump(self.settings, jsonfile, ensure_ascii=True, indent=4)

    
