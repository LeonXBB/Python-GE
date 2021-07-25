import math
from engine.threadClass import threadClass

class Task:

    def __init__(self, mainThread, frame, instruction, group='') -> None:
        
        self.mainThread = mainThread

        self.frame = frame
        self.instruction = instruction
        self.group = group

    def execute(self):
        exec(self.instruction)

class updateThread(threadClass):

    def to(self, to, value):

        if to == 'i':
            return math.ceil(value / self.updateFrequency)
        elif to == 'seconds':
            return value * self.updateFrequency

    def getInsertIndex(self, taskData, before=False):
        
        indexes = [int(self.tasks[i].frame) for i in range(len(self.tasks))]
        taskData[0] = int(taskData[0])

        if taskData[0] < self.i: taskData[0] = self.i

        closestLowerIndex = None
        closestHigherIndex = None
        startIndex = None
        endIndex = None

        for i in range(len(indexes)):
            if indexes[i] < taskData[0]: closestLowerIndex = i
            if indexes[i] == taskData[0] and startIndex is None: startIndex = i
            if indexes[i] == taskData[0]: endIndex = i
            if indexes[i] > taskData[0] and closestHigherIndex is None: closestHigherIndex = i 

        if closestLowerIndex is None: closestLowerIndex = -1
        if closestHigherIndex is None: closestHigherIndex = len(self.tasks)-1

        if before: rv = (startIndex if startIndex is not None else closestLowerIndex+1)
        else: rv = (endIndex if endIndex is not None else closestHigherIndex+1)

        return rv

    def addTask(self, task, before=False):

        self.freezeExecution = True
        
        task = [task.get('frame'), task.get('task'), task.get('group')]

        if task[0] is None:
            task.insert("0", task)

        self.tasks.insert(self.getInsertIndex(task, before), Task(self, *task))
 
        self.freezeExecution = False

    def removeTask(self, by, value):

        '''
        Method to remove task from the list of tasks.

        str "by" - base for removal, i.e. "frame" (remove all from the frame with index "value"), "instruction" (remove all instances  of given instruction "value"), "group" (remove all instructions that belong to the group "value).

        str\int "value" - parameter for "by".  See above for more information.
        
        #TODO add more control, i.e ability to mix multiple "by", and add subparameters to specify how "value" should be treated with respect to "by". For example, if "by" == 'instruction", currently we will delete all instruction that are equal to "value". But what if they were added by for loop with a running index. We could set optional future parameter "equality" to strict / startsWith / endsWith etc. Optionally, we could leave it as low-level function and built some interface(s) on it.
        '''
        
        for task in self.tasks:
            
            if getattr(task, by) == value:
                self.tasks.remove(task)

    def updateTasksOrder(self): #TODO write it
        
        '''
        Yet to be implemented method to restore correct tasks order should they mix up.
        '''

        pass 

    def getTasks(self):

        rv = []

        while len(self.tasks) > 0 and eval(self.tasks[0].frame) == self.i:
            rv.append(self.tasks[0])
            self.tasks = self.tasks[1:]

        return rv

    def pauseGroups(self):

        for task in self.tasks:
            for pausedGroup in self.pausedGroups:
                if task.group in pausedGroup:

                    if '0+' in task.frame:
                        task.frame = task.frame.split('+', maxSplit=2)
                        task.frame = '0+' + str(int(task.frame[1]) + 1) + '+' + task.frame[2]
                    
                    else:
                        task.frame = '0+1+' + task.frame
                
    def execute(self, dt): #TODO add parallel processing to both receiving tasks and executing them
        
        while True:
            
            if not self.freezeExecution:

                self.pauseGroups()

                for task in self.getTasks():
                    task.execute()
                    
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