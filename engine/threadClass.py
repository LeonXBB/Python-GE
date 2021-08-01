import multiprocessing
from os import stat

class threadClass(multiprocessing.Process):

    def __getstate__(self):
        state = self.__dict__.copy()
        for key in state.keys():
            state[key] = None
        return state

    def __reduce__(self):
        return super().__reduce__()

    def __init__(self, engine, **kwargs):
        
        super().__init__(target=self.loop, args=(self,))
        
        self.update(**kwargs)

        self.engine = engine
        self.addons = self.getAddons()

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

    def loop(self):
        print("HERE1234567890")
        while not self.threadLoopOverWrittenFlag:
            pass