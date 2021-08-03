import math
from engine.threadClass import threadClass

class Task:

    def __init__(self, mainThread, frame, instruction, group) -> None:
        
        self.mainThread = mainThread
        self.engine = self.mainThread.engine

        self.frame = frame
        self.instruction = instruction
        self.group = group

    def execute(self):
        exec(self.instruction)

class updateThread(threadClass):

    def incI(self, dt):
        print("I: ", str(self.i))
        self.i+=1

    def to(self, to, value):

        if to == 'i':
            return math.ceil(value / self.updateFrequency)
        elif to == 'seconds':
            return value * self.updateFrequency

    def loop(self, dt):
        
        self.waitForOtherThreads()

        while True:
            if not self.threadStopFlag:
                self.executeAddons()