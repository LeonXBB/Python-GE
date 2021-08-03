import importlib
import ctypes
from multiprocessing.shared_memory import SharedMemory
import faulthandler

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
        
        #rv = {}
        with open('logSave.txt', 'a') as f:
            faulthandler.enable(file=f)

            keys = ['engineSettings', 'appSettings', 'window', 'loadedAddons', *(addon for addon in self.appSettings.addons.keys() if self.appSettings.addons.get(addon)), 'GUIThread', 'audioThread', 'controlsThread', 'updateThread', 'internetThread', 'appThread', 'threads']
            
            for key in keys:
                try:
                    #rv[key] = id(getattr(self, key))
                    #keyID = id(getattr(self, key))
                    objID = getattr(self, key)
                    print("SAVE", key)
                    #sm = SharedMemory(name=key, size=len(keyID))
                    #sm.buf = keyID
                    sm = SharedMemory(name=key, create=True, size=objID.__sizeof__())
                    sm.buf = objID
                    print(repr(sm.buf))
                except: 
                    continue
            
            #rv["self"] = id(self)

            return keys

    def __setstate__(self, state):
        
        with open('logLoad.txt', 'a') as f:
            faulthandler.enable(file=f)

            for key in state:
                print("LOAD", key)
                #setattr(self, key, ctypes.cast(state.get(key), ctypes.py_object).value)
                sm = SharedMemory(name=key)
                print(sm.buf)
                keyID = sm.buf
                setattr(self, key, ctypes.cast(keyID, ctypes.py_object.value))

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