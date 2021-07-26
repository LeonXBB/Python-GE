class Addon:

    def __init__(self, engine, name):

        self.engine = engine
        self.name = name

        self.addonStoppedFlag = False
        self.addonBeingExecutedFlag = False

    def ensureFlags(self):    
        
        for threadName in self.relatedFlags.keys:
            
            for thread in self.engine.threads:
                
                if thread.threadName == threadName:
                    for flag in self.file.get('relatedFlag').get('threadName'):
                        setattr(thread, flag[0], flag[1])
            
                for subthread in thread.threads:
                    if subthread.threadName == threadName:
                        for flag in self.file.get('relatedFlag').get('threadName'):
                            setattr(subthread, flag[0], flag[1])

    def _launch(self):
        
        self.addonStoppedFlag = False
        self.addonBeingExecutedFlag = True
        self.ensureFlags()
        self.func()
        self.addonBeingExecutedFlag = False

    def _stop(self):
        
        self.addonStoppedFlag = True
        self.addonBeingExecutedFlag = False
        self.engine.updateThread.removeTask('group', self.name)
