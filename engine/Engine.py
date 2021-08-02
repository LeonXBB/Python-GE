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

class Engine: #settings, pipes, threads, addons, window - (clock, screenManager)

    '''def __getstate__(self):
        state = self.__dict__.copy()
        return state
      
    def __setstate__(self, state):      
        self.__dict__.update(state)''' 

    def __init__(self):
        
        self.loadSettings()
        self.window = Window()
        #self.pipes = self.getPipes(6)
        self.loadedAddons = self.loadAddons()

    def initThreads(self):

        self.GUIThread = GUIThread(self.pipes[0][1], threadName='GUI')
        self.audioThread = audioThread(self.pipes[1][1], threadName='Audio', threads=[], address=self.engineSettings.audioDefaultAddress, volume=self.engineSettings.audioVolume, extension=self.engineSettings.audioDefaultExtension, excludedTracks=self.appSettings.audioExcludedTracks, delay=0)
        self.controlsThread = controlsThread(self.pipes[2][1], threadName='Controls', mapKeysFunctions=self.appSettings.mapKeysFunctions, mapFunctionInstructions=JSONFile('keysMap'))
        self.updateThread = updateThread(self.pipes[3][1], threadName='Update', i=0, tasks=[], pausedGroups=[], updateFrequency=self.engineSettings.updateFrequency)
        self.internetThread = internetThread(self.pipes[4][1], threadName='Internet')

        self.appThread = None

        self.threads = [self.GUIThread, self.audioThread, self.controlsThread, self.updateThread, self.internetThread]
        
    def start(self):

        for thread in self.threads: thread.start()

        self.window.run()

    '''def getPipes(self, amount):

        rv = []

        for i in range(amount):
            rv.append(multiprocessing.Pipe())
            rv[-1][0].send(self)

        return rv'''

    def loadAddons(self):
        
        rv = {}

        for addon in self.appSettings.addons.keys():
            if self.appSettings.addons.get(addon):

                pipe = multiprocessing.Pipe()
                pipe[0].send(self)

                try:
                    addonModule = importlib.import_module('engine.addons.' + addon)
                except:
                    addonModule = importlib.import_module('app.addons.' + addon)
                
                classObject = getattr(addonModule, addon)
                
                rv[addon] = classObject(pipe[1], addon)
                
        return rv

    def changeSettings(self): #TODO write it
        pass

    def loadSettings(self):

        self.engineSettings = Settings('engine')
        self.appSettings = Settings('app')      
        self.engineSettings.applyValues()
        self.appSettings.applyValues()