import importlib

from engine.JSONFile import JSONFile as JSONFile
from engine.Settings import Settings as Settings
from engine.threadClass import threadClass as threadClass

from engine.core.GUI import GUIThread as GUIThread
from engine.core.Audio import audioThread as audioThread
from engine.core.Controls import controlsThread as controlsThread
from engine.core.Update import updateThread as updateThread
from engine.core.Internet import internetThread as internetThread

from engine.threadClass import threadClass

from engine.gfx.Window import Window

class Engine: #settings, pipes, threads, addons, window - (clock, screenManager)

    def getAttrsAddresses(self):
        
        rv = {}
        keys = ['engineSettings', 'appSettings', 'window', 'loadedAddons', *(addon for addon in self.appSettings.addons.keys() if self.appSettings.addons.get(addon)), 'dummyThread', 'GUIThread', 'audioThread', 'controlsThread', 'updateThread', 'internetThread', 'appThread', 'threads']
        
        for key in keys:

            try:
                keyID = id(getattr(self, key))
                rv[key] = keyID
            except Exception as e:
                continue

        return rv

    def __init__(self):

        self.loadSettings()
        self.loadedAddons = self.loadAddons()
        self.window = Window()

    def initThreads(self):

        #self.dummyThread = threadClass(threadName='dummy')
        self.GUIThread = GUIThread(threadName='GUI')
        self.audioThread = audioThread(threadName='Audio', threads=[], address=self.engineSettings.audioDefaultAddress, volume=self.engineSettings.audioVolume, extension=self.engineSettings.audioDefaultExtension, excludedTracks=self.appSettings.audioExcludedTracks, delay=0)
        self.controlsThread = controlsThread(threadName='Controls', mapKeysFunctions=self.appSettings.mapKeysFunctions, mapFunctionInstructions=JSONFile('keysMap'))
        self.updateThread = updateThread(threadName='Update', i=0, tasks=[], pausedGroups=[], updateFrequency=self.engineSettings.updateFrequency)
        self.internetThread = internetThread(threadName='Internet')

        self.appThread = None

        #self.threads = [self.dummyThread, self.GUIThread, self.audioThread, self.controlsThread, self.updateThread, self.internetThread]
        self.threads = [self.GUIThread, self.audioThread, self.controlsThread, self.updateThread, self.internetThread]

        with open("NEWIDEATEST.txt", 'a') as f:
            print('Default engine address', str(id(self)), file=f)
            print('Default engine dict', str(self.__dict__), file=f)

    def start(self):

        for addon in self.loadedAddons.keys(): self.loadedAddons.get(addon).getEngine(id(self), self.__dict__)
        for thread in self.threads: thread.getEngine(id(self), self.__dict__)

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
                
                rv[addon] = classObject(addon)
                
        return rv

    def getObject(self, objectName):
        return id(getattr(self, objectName))

    def changeSettings(self): #TODO write it
        pass

    def loadSettings(self):

        self.engineSettings = Settings('engine')
        self.appSettings = Settings('app')      
        self.engineSettings.applyValues()
        self.appSettings.applyValues()