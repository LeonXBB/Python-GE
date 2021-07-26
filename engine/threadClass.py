import threading

class threadClass(threading.Timer):

    def __init__(self, engine, **kwargs):
        
        super().__init__(interval=0, function=self.loop, args=(self,))
        
        self.update(**kwargs)

        self.engine = engine
        self.addons = self.getAddons()

        self.currentAddon = None

        self.daemon = True
        self.threadStopFlag = False
        self.threadLoopOverWrittenFlag = False

    def getAddons(self):

        rv = []

        for loadedAddon in self.engine.loadedAddons:
            if self.threadName in loadedAddon.threadsConcernded: 
                rv.append(loadedAddon)

        return rv

    def update(self, **kwargs):
        
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs.get(kwarg))

    def executeAddons(self):
        
        for addon in self.addons:
            if not addon.addonStoppedFlag and not addon.addonBeingExecutedFlag:
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

    def loop(self, dt):

        while not self.threadLoopOverWrittenFlag:
            pass