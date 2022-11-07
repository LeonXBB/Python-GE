import ctypes

class Addon:

    def __init__(self, name):

        self.name = name
        self.addonStoppedFlag = False
        self.addonBeingExecutedFlag = False

    def getEngine(self, engineAddress, dict):

        self.engine = ctypes.cast(engineAddress, ctypes.py_object).value
        self.engine.__dict__.update(dict)

    def ensureFlags(self):    
        
        for threadName in self.relatedFlags.keys():
            
            for thread in self.engine.threads:
                
                if thread.threadName == threadName:
                    for flag in self.relatedFlags.get(threadName):
                        setattr(thread, flag[0], flag[1])
            
                if hasattr(thread, 'threads'):
                    for subthread in thread.threads:
                        if subthread.threadName == threadName:
                            for flag in self.relatedFlags.get(threadName):
                                setattr(subthread, flag[0], flag[1])

    def _launch(self, engine_address=None, dict=None):
        if not hasattr(self, "engine"):
            self.getEngine(engine_address, dict)

        self.addonStoppedFlag = False
        self.addonBeingExecutedFlag = True
        self.ensureFlags()
        self.func()
        self.addonBeingExecutedFlag = False

    def _stop(self):
        
        self.addonStoppedFlag = True
        self.addonBeingExecutedFlag = False
        self.engine.updateThread.removeTask('group', self.name)

    def _pause(self):
        self.addonStoppedFlag = True

    def _resume(self):
        self.addonStoppedFlag = False