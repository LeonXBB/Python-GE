from math import e
from engine.JSONFile import JSONFile
from engine.threadClass import threadClass

from pynput import keyboard

class controlsThread(threadClass):
    
    def onPress(self, key):
        pass

    def onRelease(self, key):

        if 'KeyCode' in str(type(key)):
            givenKey = key.char
        else:
            givenKey = str(key)

        command = self.mapKeysFunctions.get(givenKey)
        instruction = self.mapFunctionInstructons.getValue(command)

        if not self.freezeKeyboardFlag:

            try:
                exec(instruction)
            except:
                pass

    def loop(self, dt):
            
            self.threadLoopOverWrittenFlag = True

            self.freezeKeyboardFlag = True

            with keyboard.Listener(on_press=self.onPress, on_release=self.onRelease) as listener: 
                listener.join()

            while True:
                if not self.engine.controlsThread.threadStopFlag:
                    pass