import threading

class threadClass(threading.Timer):

    def __init__(self, engine, **kwargs):
        
        super().__init__(interval=0.5, function=self.loop, args=(self,))
        
        self.engine = engine
        
        self.daemon = True
        self.threadStopFlag = False
        self.threadLoopOverWritenFlag = False

    def loop(self, dt):

        while not self.threadLoopOverWritenFlag:
            pass