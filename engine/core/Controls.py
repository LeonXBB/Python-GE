from engine.JSONFile import JSONFile
from engine.threadClass import threadClass

class controlsThread(threadClass):
    
    def loop(self, dt):
            
        self.waitForOtherThreads()

        while True:
            if not self.threadStopFlag:
                self.executeAddons()
