from engine.JSONFile import JSONFile as JSONFile
from kivy.config import Config

class Settings:

    def __init__(self, settingsType):

        self.settingsType = settingsType

        try: self.file = JSONFile(self.settingsType + 'Settings')
        except FileNotFoundError: self.file = None

        if self.settingsType == 'engine': 
            
            if self.file is None: self.parameters = ['engineVersion', 'audioVolume', 'audioExcludedTracks', 'windowFullscreen', 'windowWidth', 'windowHeight', 'updateFrequency']
            else: self.parameters = list(self.file.get_all_values().keys())

            self.default_values = ['0.1 Alpha', 0, [3,4,5], True, 1920, 1280, 0.04]

        elif self.settingsType == 'app':

            if self.file is None: self.parameters = ['appVersion', 'appLanguage', 'keysMap']
            else: self.parameters = list(self.file.get_all_values().keys())

            self.default_values = ['0.1 Alpha', 'EN', {}]

        self.load_values((self.file is None))

    def load_values(self, default=False):
        
        if default:
            for i in range(len(self.parameters)):
                setattr(self, self.parameters[i], self.default_values[i])

        else:
            for parameter in self.parameters:
                setattr(self, parameter, self.file.get_value(parameter))

    def apply_values(self):

        if self.settingsType == 'engine':
            
            Config.set('kivy', 'exit_on_escape', '0')
            Config.set('graphics', 'fullscreen', self.windowFullscreen)
            Config.set('graphics', 'resizable', False)
            Config.set('graphics', 'width', self.windowWidth)
            Config.set('graphics', 'height', self.windowHeight)

    def set_values(self):
        pass