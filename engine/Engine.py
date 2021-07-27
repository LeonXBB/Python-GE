import importlib

from engine.JSONFile import JSONFile as JSONFile
from engine.Settings import Settings as Settings

from engine.core.GUI import GUIThread as GUIThread
from engine.core.Audio import audioThread as audioThread
from engine.core.Controls import controlsThread as controlsThread
from engine.core.Update import updateThread as updateThread
from engine.core.Internet import internetThread as internetThread

from kivy.app import App

from kivy.clock import Clock

from kivy.uix.screenmanager import ScreenManager, NoTransition

class Engine(App): #settings, clock, screenManager, threads, addons

    def __init__(self, **kwargs):
        
        super().__init__(**kwargs)

        self.screenManager = None

        self.engineSettings = Settings('engine')
        self.appSettings = Settings('app')      
        self.loadSettings()

        self.clock = Clock       

        self.loadedAddons = self.loadAddons()

        self.GUIThread = GUIThread(self, threadName='GUI', screenManager=ScreenManager(transition=NoTransition()))
        self.audioThread = audioThread(self, threadName='Audio', threads=[], address=self.engineSettings.audioDefaultAddress, volume=self.engineSettings.audioVolume, extension=self.engineSettings.audioDefaultExtension, excludedTracks=self.appSettings.audioExcludedTracks, delay=0)
        self.controlsThread = controlsThread(self, threadName='Controls', mapKeysFunctions=self.appSettings.mapKeysFunctions, mapFunctionInstructions=JSONFile('keysMap'))
        self.updateThread = updateThread(self, threadName='Update', i=0, tasks=[], pausedGroups=[], updateFrequency=self.engineSettings.updateFrequency)
        self.internetThread = internetThread(self, threadName='Internet')

        self.threads = [self.GUIThread, self.audioThread, self.controlsThread, self.updateThread, self.internetThread]

    def build(self, **kwargs):

        super().__init__(**kwargs)

        return self.GUIThread.screenManager

    def start(self):

        for thread in self.threads:
            thread.start()

        self.run()
 
    def loadAddons(self):
        
        rv = {}

        for addon in self.appSettings.addons.keys():
            if self.appSettings.addons.get(addon):
                
                try:
                    addonModule = importlib.import_module('engine.addons.' + addon)
                except:
                    addonModule = importlib.import_module('app.addons.' + addon)
                
                classObject = getattr(addonModule, addon)
                
                rv[addon] = classObject(self, addon)
                
        return rv

    def changeSettings(self): #TODO write it
        pass

    def loadSettings(self):
        self.engineSettings.applyValues()
        self.appSettings.applyValues()