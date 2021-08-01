from engine.threadClass import threadClass

from app.gfx.screens.LoadingScreen import LoadingScreen as loadingScreen
from app.gfx.screens.StartingScreen import StartingScreen as startingScreen

class GUIThread(threadClass):
    
    def switchCoordinates(self, setCoords, systemIn, systemOut, widgetSize=None, widgetPos=None, coordsLimits=None):

        #systemsIn/Out: pixels, (geographical) coordinates, percentage
        #coordsLimits reserved for GPS

        rv = []
        coords = []

        if widgetSize is None: widgetSize = (self.engine.engineSettings.windowWidth, self.engine.engineSettings.windowHeight)
        if widgetPos is None: widgetPos = (0,0)

        dx = widgetSize[0] / 100
        dy = widgetSize[1] / 100

        for i in range(0, len(setCoords), 2):
            coords = [setCoords[i], setCoords[i+1]]

            if systemIn == 'percentage':
                
                if systemOut == 'pixels':
                    
                    rv.append(coords[0] * dx + widgetPos[0]) 
                    rv.append(coords[1] * dy + widgetPos[1])

            elif systemIn == 'pixels':

                if systemOut == 'percentage':

                    rv.append((coords[0] - widgetPos[0]) / dx)
                    rv.append((coords[1] - widgetPos[1]) / dy)

        return rv

    def pushPastIntro(self):

        '''sS = startingScreen(self.engine, True)
        self.engine.window.screenManager.add_widget(sS)
        self.engine.window.screenManager.current = 'Starting Screen'''
        pass

    def showIntro(self):

        '''lS = loadingScreen(self.engine, True)
        self.engine.window.screenManager.add_widget(lS)
        self.engine.window.screenManager.current = 'Loading Screen'
        import time 
        time.sleep(2.5)
        self.engine.updateThread.addTask({"task": "self.engine.controlsThread.freezeKeyboardFlag = False", "group": "Controls"})
        self.engine.updateThread.addTask({"task": "self.engine.GUIThread.pushPastIntro()", "group": "GUI"})
        self.engine.updateThread.addTask({"task": "self.engine.audioThread.playAllTracksFlag = [True, True]", "group": "Audio"})'''

    def loop(self, dt):
        
        self.threadLoopOverWrittenFlag = True
        self.screenManagerPassedFlag = False 

        ''' while not self.screenManagerPassedFlag:
            try:
                self.showIntro()
                self.screenManagerPassedFlag = True
            except:
                pass'''

        while True:
            if not self.threadStopFlag:
                self.executeAddons()
