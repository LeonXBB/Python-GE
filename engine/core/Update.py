import math
from engine.threadClass import threadClass

class updateThread(threadClass):

    def to(self, to, value):

        if to == 'i':
            return math.ceil(value / self.updateFrequency)
        elif to == 'seconds':
            return value * self.updateFrequency

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

    def removeTask(self, by, value):

        '''
        Method to remove task from the list of tasks.

        str "by" - base for removal, i.e. "frame" (remove all from the frame with index "value"), "instruction" (remove all instances  of given instruction "value"), "group" (remove all instructions that belong to the group "value).

        str\int "value" - parameter for "by".  See above for more information.
        
        #TODO add more control, i.e ability to mix multiple "by", and add subparameters to specify how "value" should be treated with respect to "by". For example, if "by" == 'instruction", currently we will delete all instruction that are equal to "value". But what if they were added by for loop with a running index. We could set optional future parameter "equality" to strict / startsWith / endsWith etc. Optionally, we could leave it as low-level function and built some interface(s) on it.
        '''
        
        for task in self.tasks

    def updateTasksOrder(self): #TODO write it
        
        '''
        Yet to be implemented method to restore correct tasks order should they mix up.
        '''

        pass 

    def getInstructions(self):

        rv = []

        while len(self.tasks) > 0 and eval(self.tasks[0][0]) == self.i:
            rv.append(self.tasks[0][1])
            self.tasks = self.tasks[1:]

        return rv

    def execute(self, dt): #TODO add threading if there are multiple instructions
        
        while True:
            
            if not self.freezeExecution:

                for instruction in self.getInstructions():
                    exec(instruction)

            self.i += 1
            return True

    def loop(self, dt):
        
        self.threadLoopOverWrittenFlag = True

        self.freezeExecution = False
        self.clockStartedFlag = False

        while True:
            if not self.threadStopFlag:
                if not self.clockStartedFlag:
                    self.engine.clock.schedule_interval(self.execute, self.updateFrequency)
                    self.clockStartedFlag = True