from engine.threadClass import threadClass

class internetThread(threadClass):

    def loop(self, dt):

        self.threadLoopOverWrittenFlag = True

        while True:
            if not self.threadStopFlag:
                self.executeAddons()
