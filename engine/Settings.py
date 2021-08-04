from engine.JSONFile import JSONFile as JSONFile
from kivy.config import Config

class Settings:

    def __reduce__(self):
        (self.__class__, ())

    def __init__(self, settingsType):

        self.settingsType = settingsType

        try: self.file = JSONFile(self.settingsType + 'Settings')
        except FileNotFoundError: self.file = None

        if self.settingsType == 'engine': 
            
            if self.file is None: self.parameters = ['engineVersion', 'engineExitOnEscape', 'engineClockType', 'audioVolume', 'audioDefaultAddress', 'audioDefaultExtension', 'audioAppendOn', 'windowResizable', 'windowFullscreen', 'windowWidth', 'windowHeight', 'windowShowCursor' 'updateFrequency']
            else: self.parameters = list(self.file.getAllValues().keys())

            self.defaultValues = ['0.1 Alpha', 0, 'default', 0, './app/audio/', '.wav', 'start', False, True, 1920, 1280, 0, 0.04]

        elif self.settingsType == 'app':

            if self.file is None: self.parameters = ['appVersion', 'appLanguage', 'audioExcludedTracks', 'audioIfBeingPlayedTrackOrderRandomized', 'audioAllowTrackRepeatAtCycleEndStart', 'mapKeysFunctions', 'addons']
            else: self.parameters = list(self.file.getAllValues().keys())

            self.defaultValues = ['0.1 Alpha', 'EN', [3,4,5], 'cycle', 0, {}, {}]

        self.loadValues()

    def loadValues(self):
        
        for i in range(len(self.parameters)):
            
            try:
                setattr(self, self.parameters[i], self.file.getValue(self.parameters[i]))
            except:
                setattr(self, self.parameters[i], self.defaultValues[i])

    def applyValues(self):

        if self.settingsType == 'engine':
            
            Config.set('kivy', 'exit_on_escape', self.engineExitOnEscape)
            Config.set('kivy', 'kivy_clock', self.engineClockType)
            Config.set('graphics', 'show_cursor', self.windowShowCursor)
            Config.set('graphics', 'resizable', self.windowResizable)
            Config.set('graphics', 'fullscreen', self.windowFullscreen)
            Config.set('graphics', 'width', self.windowWidth)
            Config.set('graphics', 'height', self.windowHeight)

    def setValues(self): # TODO write it
        pass