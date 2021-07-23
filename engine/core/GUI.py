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

    def pushPastIntro(self, dt):

        sS = startingScreen(self.engine, True)
        self.engine.screenManager.add_widget(sS)
        self.engine.screenManager.current = 'Starting Screen'

    def showIntro(self):

        lS = loadingScreen(self.engine, True)
        self.engine.screenManager.add_widget(lS)
        self.engine.screenManager.current = 'Loading Screen'
        import time 
        time.sleep(2.5)
        self.engine.updateThread.addTask("self.engine.controlsThread.freezeKeyboardFlag = False")
        self.engine.updateThread.addTask("self.engine.GUIThread.pushPastIntro()")
        self.engine.updateThread.addTask("self.engine.audioThread.playAllTracksFlag = [True, True]")

    def loop(self, dt):
        
        self.threadLoopOverWrittenFlag = True

        self.screenManagerPassedFlag = False 

        while True:
            if not self.threadStopFlag:
               
                while not self.screenManagerPassedFlag:
                    
                    try:
                        self.showIntro()
                        self.screenManagerPassedFlag = True
                    except:
                        pass