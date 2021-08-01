import importlib
import multiprocessing

from engine.JSONFile import JSONFile as JSONFile
from engine.Settings import Settings as Settings
from engine.threadClass import threadClass as threadClass

from engine.core.GUI import GUIThread as GUIThread
from engine.core.Audio import audioThread as audioThread
from engine.core.Controls import controlsThread as controlsThread
from engine.core.Update import updateThread as updateThread
from engine.core.Internet import internetThread as internetThread

from engine.gfx.Window import Window

class Engine: #settings, threads, addons, window - (clock, screenManager)

    def __getstate__(self):
        state = self.__dict__.copy()
        for key in state.keys():
            state[key] = None
        return state

    def __reduce__(self):
        return super().__reduce__()

    def __init__(self):
        
        self.engineSettings = Settings('engine')
        self.appSettings = Settings('app')      
        self.loadSettings()

        self.loadedAddons = self.loadAddons()

        self.GUIThread = GUIThread(self, threadName='GUI')
        self.audioThread = audioThread(self, threadName='Audio', threads=[], address=self.engineSettings.audioDefaultAddress, volume=self.engineSettings.audioVolume, extension=self.engineSettings.audioDefaultExtension, excludedTracks=self.appSettings.audioExcludedTracks, delay=0)
        self.controlsThread = controlsThread(self, threadName='Controls', mapKeysFunctions=self.appSettings.mapKeysFunctions, mapFunctionInstructions=JSONFile('keysMap'))
        self.updateThread = updateThread(self, threadName='Update', i=0, tasks=[], pausedGroups=[], updateFrequency=self.engineSettings.updateFrequency)
        self.internetThread = internetThread(self, threadName='Internet')

        self.threads = [self.GUIThread, self.audioThread, self.controlsThread, self.updateThread, self.internetThread]
        
    def start(self):

        self.window = Window()

        pool = multiprocessing.Pool(processes=len(self.threads))
        pool.map(threadClass.super().start, self.threads)
 
        self.window.run()

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