import multiprocessing
import threading
import ctypes

#class threadClass(multiprocessing.Process):
class threadClass(threading.Thread):

    def __init__(self, **kwargs):
        
        super().__init__(target=self.loop, args=(self,))
        
        self.update(**kwargs)

        self.engine = None

        self.daemon = True
        self.threadStopFlag = False
        self.threadLoopOverWrittenFlag = False

    def getEngine(self, engineAddress, newDict):

        self.engine = ctypes.cast(engineAddress, ctypes.py_object).value
        self.engine.__dict__.update(newDict)
        self.engineAddress = engineAddress
        self.newDict = newDict
        self.addons = self.getAddons()
        self.currentAddon = None

        with open("NEWIDEATEST.txt", 'a') as f:
            print('New Thread name', self.threadName, file=f)
            print('New Thread engine address', str(id(self.engine)), file=f)
            print('New Thread engine dict', str(self.engine.__dict__), file=f)
     
    def update(self, **kwargs):
        
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs.get(kwarg))

    def getAddons(self):

        rv = []

        for loadedAddon in self.engine.loadedAddons.keys():
            if self.threadName in self.engine.loadedAddons.get(loadedAddon).threadsConcerned: 
                rv.append(self.engine.loadedAddons.get(loadedAddon))

        return rv

    def executeAddons(self):  #TODO multiprocess
        
        for addon in self.addons:
            if not addon.addonStoppedFlag and not addon.addonBeingExecutedFlag and addon.autostart:
                addon.start()
                self.currentAddon = addon

    def _start(self):
        
        self.threadStopFlag = False

    def _resume(self):
        
        self.threadStopFlag = False
        self.engine.updateThread.pausedGroups.remove(self.threadName)

    def _pause(self):

        self.threadStopFlag = True       
        self.engine.updateThread.pausedGroups.append(self.threadName)

    def _stop(self): # TODO add defaulting all nonStop flags to False
         
        self.threadStopFlag = True
        self.engine.updateThread.removeTask('group', self.threadName)

    def waitForOtherThreads(self):
        
        i = 0

        while self.engine is None or not hasattr(self.engine, 'threads') or len(self.engine.threads) < 5:
            if i == 0: 
                with open("NEWIDEATEST.txt", 'a') as f:
                    print('SELF DICT', str(self.__dict__), file=f)
                    #print("SELF FUNCTION DICT", str(self.newDict), file=f)
                    if self.engine is not None: print('SELF ENGINE DICT', str(self.engine.__dict__), file=f)
                i+=1
            else: pass

    def loop(self, dt):

        self.waitForOtherThreads()
        while True: pass