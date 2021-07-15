from engine.threadClass import threadClass

from pynput import keyboard

import sys

class controlsThread(threadClass):
    
    def loop(self, dt):
            
            self.threadLoopOverWrittenFlag = True

            while not self.engine.controlsThread.threadStopFlag:
            
                global threads 
                threads = [self.engine.GUIThread, self.engine.audioThread, self.engine.controlsThread, 
                self.engine.timeThread, self.engine.internetThread]

                def on_press(key):
                    pass

                def on_release(key):

                    if key == keyboard.Key.esc:
                        
                        for thread in threads: 
                            try:
                                thread.threadStopFlag = True
                            except:
                                pass

                        sys.exit()

                with keyboard.Listener(on_press=on_press, on_release=on_release) as listener: 
                    listener.join()