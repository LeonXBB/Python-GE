from engine.Addon import Addon

class ShowIntro(Addon):
    
    def start(self):

        self.threadsConcernded = ['GUI']
        self.relatedFlags = {}
        self._launch() 

    def stop(self):
        self._stop()

    def func(self):
        
        '''lS = loadingScreen(self.engine, True)
        self.engine.screenManager.add_widget(lS)
        self.engine.screenManager.current = 'Loading Screen'
        import time 
        time.sleep(2.5)'''
        self.engine.updateThread.addTask({"task": "self.engine.controlsThread.freezeKeyboardFlag = False", "group": "Controls"})
        self.engine.updateThread.addTask({"task": "self.engine.GUIThread.pushPastIntro()", "group": "GUI"})
        self.engine.updateThread.addTask({"task": "self.engine.audioThread.playAllTracksFlag = [True, True]", "group": "Audio"})