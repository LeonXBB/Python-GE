from timeit import default_timer as timer
import time

from engine.threadClass import threadClass

class updateThread(threadClass):

    #century, year, month, week, day, 

    def addInstruction(self, instruction, index, before_after=None):

        while len(self.instructions) < index:
            self.instructions.append([]) 
            
        self.instructions[index].append(str(instruction) + '\n')

    def removeInstruction(self, instruction, index):

        self.instructions[index].remove(str(instruction) + '\n')

    def getInstructions(self):

        rv = []

        while len(self.tasks) > 0 and eval(self.tasks[0][0]) == self.i:
            rv.append(self.tasks[0][1])
            self.tasks = self.tasks[1:]

        return rv

    def execute(self, dt):
        
        for instruction in self.getInstructions():
            exec(instruction)

        self.i += 1

    def loop(self, dt):
        
        self.threadLoopOverWrittenFlag = True

        self.i = 0

        #self.tasks = []
        self.tasks = [["0","print('Hello')"],["0","print(' again ')"],["1","print('there, ')"],["2","print('darkness')"],["3","print(', my old')"],["4","print('friend')"]]

        while not self.threadStopFlag:

            self.engine.clock.schedule_interval(self.execute, self.engine.engineSettings.updateFrequency)
            '''timeStart = timer() 

            for instruction in self.getInstructions():
                exec(instruction)            

            timeEnd = timer()

            if self.engine.engineSettings.updateFrequency - (timeEnd - timeStart) > 0:
                time.sleep(max(0, self.engine.engineSettings.updateFrequency - (timer() - timeStart)))

            self.i += 1'''
