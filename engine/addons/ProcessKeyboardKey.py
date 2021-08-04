from engine.Addon import Addon

class ProcessKeyboardKey(Addon):

    def __init__(self, name):

        super().__init__(name)
        
        self.threadsConcerned = ['Controls']
        self.relatedFlags = {"Controls": [["freezeKeyboardFlag", False]]}
        self.autostart = False
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

        from pynput import keyboard

        def onPress(self, key):
          pass

        def onRelease(self, key):

            if 'KeyCode' in str(type(key)):
                givenKey = key.char
            else:
                givenKey = str(key)

            command = self.engine.controlsThread.mapKeysFunctions.get(givenKey)
            instruction = self.engine.controlsThread.mapFunctionInstructions.getValue(command)

            if not self.freezeKeyboardFlag:

                try:
                    exec(instruction)
                except:
                    pass

        with keyboard.Listener(on_press=onPress, on_release=onRelease) as listener: 
                listener.join()
        
        self.pause()