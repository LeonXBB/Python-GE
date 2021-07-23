import math
from engine.threadClass import threadClass

class updateThread(threadClass):

    def to(self, to, value):

        if to == 'i':
            return math.ceil(value / (1000/self.updateFrequency) )
        elif to == 'seconds':
            return value * (1000/self.updateFrequency)

    def addTask(self, task, before=False):

        self.freezeExecution = True
        
        if type(task) == str or len(task) < 2:
            task = [self.i, task]

        indexes = [int(self.tasks[i][0]) for i in range(len(self.tasks))]
        task[0] = int(task[0])

        if task[0] < self.i: task[0] = self.i

        closestLowerIndex = None
        closestHigherIndex = None
        startIndex = None
        endIndex = None

        for i in range(len(indexes)):
            if indexes[i] < task[0]: closestLowerIndex = i
            if indexes[i] == task[0] and startIndex is None: startIndex = i
            if indexes[i] == task[0]: endIndex = i
            if indexes[i] > task[0] and closestHigherIndex is None: closestHigherIndex = i 

        if closestLowerIndex is None: closestLowerIndex = -1
        if closestHigherIndex is None: closestHigherIndex = len(self.tasks)-1

        if before: self.tasks.insert(startIndex if startIndex is not None else closestLowerIndex+1, [str(task[0]), task[1]])
        else: self.tasks.insert(endIndex if endIndex is not None else closestHigherIndex+1, [str(task[0]), task[1]])
 
        self.freezeExecution = False

    def removeTask(self, task):
        self.tasks.remove(task)

    def updateTasksOrder(self): #TODO write it
        pass 

    def getInstructions(self):

        rv = []

        while len(self.tasks) > 0 and eval(self.tasks[0][0]) == self.i:
            rv.append(self.tasks[0][1])
            self.tasks = self.tasks[1:]

        return rv

    def execute(self, dt):
        
        if not self.freezeExecution:

            for instruction in self.getInstructions():
                print(instruction)
                exec(instruction)

            self.i += 1

    def loop(self, dt):
        
        self.threadLoopOverWrittenFlag = True

        self.freezeExecution = False

        while True:
            if not self.threadStopFlag:
                self.engine.clock.schedule_interval(self.execute, 1000/self.updateFrequency)