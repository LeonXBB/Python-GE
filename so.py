import ctypes
import multiprocessing

class myProcessObject(multiprocessing.Process):
    
    # no explicitly written __reduce__ method as I suppose standard library objects have it by default

    def __init__(self, threadNumber):
        
        '''This is a function that creates process object'''

        super().__init__(target=self.doSomeWork, args=(self,))
        
        self.threadNumber = threadNumber
        self.daemon = False # I don't really know the difference, have read the docs, and seems like this is what I need.

        self.mainObject = None # None at first and explicitly called after to wait until all threads are created 

    def getMainObject(self, address, dict):
        
        '''The absolutely most important function in the whole code: it copies mainObject from main process to this, together with its attributes'''
        
        self.mainObject = ctypes.cast(address, ctypes.py_object).value #copying mainObject
        self.mainObject.__dict__.update(dict) #copying mainObject's dictionary...

        with open('log.txt', 'a') as f: # logging everything
            print('At Copying Thread # ' + str(self.threadNumber) + ' mainObject Memory Address:', str(id(self.mainObject)), file=f)
            print('At Copying Thread # ' + str(self.threadNumber) + ' mainObject Dictionary', str(self.mainObject.__dict__), '\n', file=f)

    def doSomeWork(self, dt):

        '''Target function of the process'''

        with open('log.txt', 'a') as f: # logging everything
            print('At Running Thread # ' + str(self.threadNumber) + ' mainObject Memory Address:', str(id(self.mainObject)), file=f)
            print('At Running Thread # ' + str(self.threadNumber) + ' mainObject Dictionary', str(self.mainObject.__dict__), '\n', file=f)

class subObjectOfMySubObject:

    "import anotherModuleFromPythonStandardLibrary" # not on the top due to every object actually being in different file

    def __reduce__(self): 
        '''__reduce__ function added due to code crashing without it.'''
        return (self.__class__, ())

    def __init__(self):
        
        '''This is a function that creates a subobject for the subobject (of the main object).
        All attribute are default built-in types, but some are returned from standards libraries'''

        self.firstAttribute = 'string' 
        self.secondAttribute = "anotherModuleFromPythonStandardLibrary.someMethod(someValues)"

class mySubObject:

    "import thirdPartyGUIModule.submodule" # not on the top due to every object actually being in different file

    def __reduce__(self): 
        '''__reduce__ function added due to code crashing without it.'''
        return (self.__class__, ())

    def __init__(self):

        '''This is a function that creates a subobject for the subobject (of the main object). 
        All attributes of the subobject are default buit-in types, except for one.'''
        
        self.firstAttribute = "string" 
        self.secondAttribute = [0,1,2]
        self.thirdAttribute = subObjectOfMySubObject()
        
        "with self.thirdAttribute as at: thirdPartyGUIModule.submodule.doSomething(at)" # GUI-related manipulations

class myGUIObject():  #class myGUIObject(thirdPartyGUIModule.mainGUIModule) - inheirits from third-party GUI module, cannot show in code due to syntax

    '''This class is an interface between GUI module and my app created with the purpose of adding __reduce__ method, as the module doesn't have it, unlike all others'''

    def __reduce__(self):
        '''__reduce__ function added due to code crashing without it.'''
        return (self.__class__, ())

    def __init__(self):
        '''This is a function that creates a GUI object.'''
        pass

    def run(self):
        '''This function represents running GUI in an endless loop.'''
        
        with open('log.txt', 'a') as f: # logging everything
            print("End of Script", file=f)
       
class myMainObject: 
    
    '''This is main loop of the programm. It does not inheirit from the ```multriprocessing.Process``` as it is already a thread itself due to the way Python works.'''

    def __reduce__(self):
        '''__reduce__ function added due to code crashing without it. Empty due to us updating the __dict__ manually later on.'''
        return (self.__class__, ())

    def __init__(self):

        '''This is a function that creates main object. First, it sets all no-processes related attributes, then the processes itself. 
        No specific reason while threads are created both as attributes and inside a list. I use list for iterations and attribute of the object for direct calls.'''

        # creating attributes other than processes
        self.attribute = mySubObject()
        self.GUI = myGUIObject()

        # creating processes
        self.processes = []
        for i in range(4):
            newProcess = myProcessObject(threadNumber=i)
            setattr(self, 'thread'+str(i), newProcess)
            self.processes.append(newProcess)

    def start(self):

        '''This is a function that starts the app.'''

        with open('log.txt', 'a') as f: # logging everything
            print('Default mainObject Memory Address:', str(id(self)), file=f)
            print('Default mainObject Dictionary:', str(self.__dict__), '\n', file=f)
        
        for process in self.processes: process.getMainObject(id(self), self.__dict__)
        for process in self.processes: process.start()

        self.GUI.run() # representation of running GUI. When user closes the GUI window, the script terminates as well.

if __name__ == "__main__":

    with open("log.txt", 'w'): pass # delete any previous log

    multiprocessing.freeze_support() # added for the future executable.

    mainThread = myMainObject()
    mainThread.start()