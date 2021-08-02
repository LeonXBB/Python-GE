from engine.JSONFile import JSONFile
from engine.threadClass import threadClass

class controlsThread(threadClass):
    
    def loop(self, dt):
            
            self.threadLoopOverWrittenFlag = True

            while True:
                if not self.threadStopFlag:
                    self.executeAddons()
