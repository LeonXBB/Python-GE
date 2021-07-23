import threading

class threadClass(threading.Timer):

    def __init__(self, engine, **kwargs):
        
        super().__init__(interval=0.5, function=self.loop, args=(self,))
        
        self.update(**kwargs)

        self.engine = engine
        
        self.daemon = True
        self.threadStopFlag = False
        self.threadLoopOverWrittenFlag = False

    def update(self, **kwargs):
        
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs.get(kwarg))

    def loop(self, dt):

        while not self.threadLoopOverWrittenFlag:
            pass