from engine.JSONFile import JSONFile
from engine.threadClass import threadClass

from pynput import keyboard

class controlsThread(threadClass):
    
    def loop(self, dt):
            
            self.threadLoopOverWrittenFlag = True

            self.keysMap = JSONFile('keysMap')

            while not self.engine.controlsThread.threadStopFlag:

                def on_press(key):
                    pass

                def on_release(key):                
                    
                    if 'KeyCode' in str(type(key)):
                        givenKey = key.char
                    else:
                        givenKey = str(key)

                    command = self.engine.appSettings.keysMap.get(givenKey)
                    instruction = self.keysMap.get_value(command)
                    if instruction is not None: exec(instruction)

                with keyboard.Listener(on_press=on_press, on_release=on_release) as listener: 
                    listener.join()