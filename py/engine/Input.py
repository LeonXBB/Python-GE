from pynput import keyboard

import sys

def inputThread(engine):
        
        while not engine.controlsThread.stopFlag:
        
            global threads 
            threads = [engine.GUIThread, engine.audioThread, engine.controlsThread, 
            engine.timeThread, engine.internetThread]

            def on_press(key):
                pass

            def on_release(key):

                if key == keyboard.Key.esc:
                    
                    for thread in threads: 
                        try:
                            thread.stopFlag = True
                        except:
                            pass

                    sys.exit()

            with keyboard.Listener(on_press=on_press, on_release=on_release) as listener: 
                listener.join()