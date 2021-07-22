import time

from engine.threadClass import threadClass

class updateThread(threadClass):

    def addInstruction(self, instruction, index):

        while len(self.instructions) < index:
            self.instructions.append([]) 
            
        self.instructions[index].append(str(instruction) + '\n')

    def removeInstruction(self, instruction, index):

        self.instructions[index].remove(str(instruction) + '\n')

    def loop(self, dt):
        
        self.threadLoopOverWrittenFlag = True

        self.currentIndex = 0

        self.instructions = [[]]

        while not self.threadStopFlag:

            timeStart = time.time() 

            for instruction in self.instructions[self.currentIndex]:
                exec(instruction)            

            timeEnd = time.time()

            if timeEnd - timeStart < self.engine.engineSettings.updateFrequency:
                time.sleep(time.time() -timeStart - self.engine.engineSettings.updateFrequency)

            self.currentIndex += 1
         