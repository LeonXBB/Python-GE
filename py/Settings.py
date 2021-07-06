from os import error
from py.JSONFile import JSONFile as JSONFile
from kivy.config import Config

class Settings:

    def __init__(self):

        self.parameters = ['appVersion', 'appLanguage', 'windowFullscreen', 'windowWidth', 'windowHeight']
        self.default_values = ['Default', 'EN', False, 1024, 600]

        try: 
            self.file = JSONFile('appSettings')
            self.load_values()

        except FileNotFoundError:
            self.load_values(True)

    def load_values(self, default=False):
        
        if default:
            for i in range(len(self.parameters)):
                setattr(self, self.parameters[i], self.default_values[i])

        else:
            for parameter in self.parameters:
                setattr(self, parameter, self.file.get_value(parameter))

    def apply_values(self):

        Config.set('graphics', 'fullscren', self.windowFullscreen)
        Config.set('graphics', 'resizable', False)
        Config.set('graphics', 'width', self.windowWidth)
        Config.set('graphics', 'height', self.windowHeight)

    def set_values(self):
        pass