from os import getcwd
from engine.Addon import Addon

class ShowIntro(Addon):
    
    def __init__(self, enginePipe, name):

        super().__init__(enginePipe, name)
        
        self.threadsConcerned = ['GUI']
        self.relatedFlags = {}
        self.autostart = True
        self.parameters = {"Background Music": False}

    def start(self):
        self._launch() 

    def stop(self):
        self._stop()

    def pause(self):
        self._pause()

    def resume(self):
        self._resume()

    def func(self):
        
        '''lS = loadingScreen(self.engine, True)
        self.engine.screenManager.add_widget(lS)
        self.engine.screenManager.current = 'Loading Screen'
        import time 
        time.sleep(2.5)
        '''
        self.engine.updateThread.addTask({"task": "self.engine.loadedAddons.get('ProcessKeyBoardKey').start()", "group": "Controls ShowIntro"})
        self.engine.updateThread.addTask({"task": "self.engine.GUIThread.pushPastIntro()", "group": "GUI ShowIntro"})
        
        if self.parameters.get('Background Music'):
            self.engine.updateThread.addTask({"task": "self.engine.loadedAddons.get('PlayBackgroundMusicInLoops').start()", "group": "Audio Thread 0 PlayBackgroundMusicInLoops"})

        self.pause()
