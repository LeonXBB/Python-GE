import importlib
import ctypes
from logging import exception
from typing import cast

from engine.JSONFile import JSONFile as JSONFile
from engine.Settings import Settings as Settings
from engine.threadClass import threadClass as threadClass

from engine.core.GUI import GUIThread as GUIThread
from engine.core.Audio import audioThread as audioThread
from engine.core.Controls import controlsThread as controlsThread
from engine.core.Update import updateThread as updateThread
from engine.core.Internet import internetThread as internetThread

from engine.gfx.Window import Window

class Engine: #settings, pipes, threads, addons, window - (clock, screenManager)
   
    def __getstate__(self):
        
        print('here222')

        rv = {}
        keys = ['engineSettings', 'appSettings', 'window', 'loadedAddons', *(addon for addon in self.appSettings.addons.keys() if self.appSettings.addons.get(addon)), 'GUIThread', 'audioThread', 'controlsThread', 'updateThread', 'internetThread', 'appThread', 'threads']
        
        for key in keys:
            try:
                rv[key] = id(getattr(self, key))
            except: 
                continue
        
        return rv

    def __setstate__(self, state):
        
        print('here333')

        for key in state.keys():
            setattr(self, key, ctypes.cast(state.get(key), ctypes.py_object).value)

    def __init__(self):
        
        self.loadSettings()
        self.window = Window()
        self.loadedAddons = self.loadAddons()

    def initThreads(self):

        self.GUIThread = GUIThread(id(self), threadName='GUI')
        self.audioThread = audioThread(id(self), threadName='Audio', threads=[], address=self.engineSettings.audioDefaultAddress, volume=self.engineSettings.audioVolume, extension=self.engineSettings.audioDefaultExtension, excludedTracks=self.appSettings.audioExcludedTracks, delay=0)
        self.controlsThread = controlsThread(id(self), threadName='Controls', mapKeysFunctions=self.appSettings.mapKeysFunctions, mapFunctionInstructions=JSONFile('keysMap'))
        self.updateThread = updateThread(id(self), threadName='Update', i=0, tasks=[], pausedGroups=[], updateFrequency=self.engineSettings.updateFrequency)
        self.internetThread = internetThread(id(self), threadName='Internet')

        self.appThread = None

        self.threads = [self.GUIThread, self.audioThread, self.controlsThread, self.updateThread, self.internetThread]
        
    def start(self):

        for thread in self.threads: thread.start()
        
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
                
                rv[addon] = classObject(id(self), addon)
                
        return rv

    def changeSettings(self): #TODO write it
        pass

    def loadSettings(self):

        self.engineSettings = Settings('engine')
        self.appSettings = Settings('app')      
        self.engineSettings.applyValues()
        self.appSettings.applyValues()