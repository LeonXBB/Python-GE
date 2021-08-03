import multiprocessing
import ctypes

class threadClass(multiprocessing.Process):

    def __init__(self, engineAddress, **kwargs):
        
        super().__init__(target=self.loop, args=(self,))
        
        self.update(**kwargs)

        self.engine = ctypes.cast(engineAddress, ctypes.py_object).value
        #self.addons = self.getAddons()

        self.currentAddon = None

        self.daemon = True
        self.threadStopFlag = False
        self.threadLoopOverWrittenFlag = False

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
        
        #print(self.threadName,  str(self.engine.__dict__))

        while not hasattr(self.engine, 'threads') or len(self.engine.threads < 5):
            pass

        print('here')