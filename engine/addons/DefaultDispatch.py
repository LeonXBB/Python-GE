from engine.Addon import Addon

class DefaultDispatch(Addon):

    def __init__(self, engineAddress, name):

        super().__init__(engineAddress, name)
        
        self.threadsConcerned = ['Update']
        self.relatedFlags = {"Update": [["freezeExecution", False], ["clockStartedFlag", False], ["freezeTasksUpdate", False]]}
        self.autostart = True
        self.parameters = {}

    def start(self):
        self._launch() 

    def stop(self):
        self._stop()

    def pause(self):
        self._pause()

    def resume(self):
        self._resume()

    def func(self):

        def getInsertIndex(self, taskData, before=False): 
        
            indexes = [int(self.tasks[i].frame) for i in range(len(self.tasks))]
            
            taskData[0] = int(taskData[0])

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
            else: rv = (endIndex+1 if endIndex is not None else closestHigherIndex+1)

            return rv

        def addTask(self, task, before=False):

            self.freezeExecution = True
            
            task = [task.get('frame'), task.get('task'), task.get('group')]
                
            if type(task[0]) == str and task[0][0] == '+': task[0] = self.i + int(task[0][1:]) 
            elif type(task[0]) == str and task[0][0] != '+': 
                task[0] = str(eval(task[0]))
                print('TASK 0: ', task[0])

            if task[0] is None: task[0] = str(self.i+1)

            #print('INSERT INDEX: ', str(self.getInsertIndex(task, before)))

            self.tasks.insert(self.getInsertIndex(task, before), Task(self, task[0], task[1], task[2]))
    
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

            while len(self.tasks) > 0 and eval(str(self.tasks[0].frame)) <= self.i:
                rv.append(self.tasks[0])
                self.tasks.pop(0)

            return rv

        def pauseGroups(self):

            for task in self.tasks:
                for pausedGroup in self.pausedGroups:
                    if task.group in pausedGroup:

                        #print("PAUSE UPDATE, CURRENT FRAME: ", task.frame)

                        if '0+' in task.frame:
                            task.frame = task.frame.split('+', maxSplit=2)
                            task.frame = '0+' + str(int(task.frame[1]) + 1) + '+' + task.frame[2]
                        
                        else:
                            task.frame = '0+1+' + task.frame
                    
                        #print("PAUSE UPDATE, UPDATED FRAME: ", task.frame)

        def execute(self, dt): #TODO add parallel processing to both receiving tasks and executing them
            
            if not self.freezeExecution:

                if not self.freezeTasksUpdate: 
                    self.pauseGroups()
                    tasksToDo = self.getTasks()
                    self.freezeTasksUpdate = True
                    #print("TASKS GOTTEN: ", str(tasksToDo))
                    for task in tasksToDo:
                        try:
                            print("TASK INSTRUCTION: ", str(task.instruction))
                            task.execute()
                            #print("TASK EXECUTED SUCCESSFULLY")
                        except:
                            #print("TASK INSTRUCTION FAILED: ", str(task.instruction))
                            raise RuntimeError

                    #print("CURRENT I: " + str(self.i+1))
                    #self.i += 1
                    self.freezeTasksUpdate = False

            return True

        setattr(self.engine.updateThread, 'getInsertIndex', getInsertIndex)
        setattr(self.engine.updateThread, 'addTask', addTask)
        setattr(self.engine.updateThread, 'removeTask', removeTask)
        setattr(self.engine.updateThread, 'updateTasksOrder', updateTasksOrder)
        setattr(self.engine.updateThread, 'getTasks', getTasks)
        setattr(self.engine.updateThread, 'pauseGroups', pauseGroups)
        setattr(self.engine.updateThread, 'execute', execute)

        if not self.clockStartedFlag:
            self.engine.window.clock.schedule_interval(self.incI, self.updateFrequency)
            self.engine.window.clock.schedule_interval(self.execute, self.updateFrequency)
            self.clockStartedFlag = True

        self.pause()