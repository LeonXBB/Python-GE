from ..JSONFile import JSONFile as JSONFile
from ..Settings import Settings as Settings

from engine.core.GUI import GUIThread as GUIThread
from engine.core.Audio import audioThread as audioThread
from engine.core.Controls import controlsThread as controlsThread
from engine.core.Update import updateThread as updateThread
from engine.core.Internet import internetThread as internetThread

from kivy.app import App

from kivy.clock import Clock

from kivy.uix.screenmanager import ScreenManager, NoTransition

class Engine(App): #settings, clock, screenManager, threads

    def __init__(self, **kwargs):
        
        super().__init__(**kwargs)

        self.screenManager = None

        self.engineSettings = Settings('engine')
        self.appSettings = Settings('app')      
        self.loadSettings()

        self.clock = Clock       

        self.GUIThread = GUIThread(self)
        self.audioThread = audioThread(self, audios=[], endTimeMark=0, address=self.engineSettings.audioDefaultAddress, volume=self.engineSettings.audioVolume, extension=self.engineSettings.audioDefaultExtension)
        self.controlsThread = controlsThread(self, mapKeysFunctions=self.appSettings.mapKeysFunctions, mapFunctionInstructions=JSONFile('keysMap'))
        self.updateThread = updateThread(self, i=0, tasks=[], updateFrequency=self.engineSettings.updateFrequency)
        self.internetThread = internetThread(self)

        self.threads = [self.GUIThread, self.audioThread, self.controlsThread, self.updateThread, self.internetThread]

    def build(self, **kwargs):

        super().__init__(**kwargs)

        self.screenManager = ScreenManager(transition=NoTransition())
        return self.screenManager

    def start(self):

        for thread in self.threads:
            thread.start()

        self.updateThread.threadStopFlag = False

        self.run()
 
    def changeSettings(self): #TODO write it
        pass

    def loadSettings(self):
        self.engineSettings.applyValues()
        self.appSettings.applyValues()