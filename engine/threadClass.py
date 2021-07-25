import threading

class threadClass(threading.Timer):

    def __init__(self, engine, **kwargs):
        
        super().__init__(interval=0.1, function=self.loop, args=(self,))
        
        self.update(**kwargs)

        self.engine = engine
        
        self.daemon = True
        self.threadStopFlag = False
        self.threadLoopOverWrittenFlag = False

    def update(self, **kwargs):
        
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs.get(kwarg))

    def _start(self):
        
        self.threadStopFlag = False

    def _resume(self):
        
        self.engine.updateThread.pausedGroups.remove(self.threadName)

    def _pause(self):
        
        self.engine.updateThread.pausedGroups.append(self.threadName)

    def _stop(self): # TODO add defaulting all nonStop flags to False
         
        self.threadStopFlag = True

        self.engine.updateThread.removeTask('group', self.threadName)

    def loop(self, dt):

        while not self.threadLoopOverWrittenFlag:
            pass