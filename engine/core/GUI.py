from engine.threadClass import threadClass
from engine.JSONFile import JSONFile

from functools import partial

from gfx.screens.LoadingScreen import LoadingScreen as loadingScreen
from gfx.screens.StartingScreen import StartingScreen as startingScreen

from kivy.uix.gridlayout import GridLayout, GridLayoutException

from kivy.graphics import *

class GUIThread(threadClass):
    
    def switchCoordinates(self, setCoords, systemIn, systemOut, widgetSize=None, widgetPos=None, coordsLimits=None):

        #systemsIn/Out: pixels, (geographical) coordinates, percentage
        #coordsLimits reserved for GPS

        rv = []
        coords = []

        if widgetSize is None: widgetSize = (self.engine.settings.windowWidth, self.engine.settings.windowHeight)
        if widgetPos is None: widgetPos = (0,0)

        dx = widgetSize[0] / 100
        dy = widgetSize[1] / 100

        for i in range(0, len(setCoords), 2):
            coords = [setCoords[i], setCoords[i+1]]

            if systemIn == 'percentage':
                
                if systemOut == 'pixels':
                    
                    rv.append(coords[0] * dx + widgetPos[0]) 
                    rv.append(coords[1] * dy + widgetPos[1])

        return rv

    def putText(self, widget, text, texture='fontTexture', coordinates='fontCoordinates', minGrid=(None, None), maxGrid=(None,None), separator=' '):
        
        def getTexture(texture):
            
                if type(texture) == str:
                    texture = JSONFile(texture).get_all_values()
                
                elif type(texture) == dict:
                    pass

                else:
                    raise TypeError

                return texture

        def getGrid(gridWidget, textToPut, minGrid, maxGrid, separator):

            textToPut = textToPut.split(separator)

            textLength = (len(textToPut) - 1) * len(separator)
            for i in range(len(textToPut)):
                textLength += len(textToPut[i])

            xLimit = (minGrid[0] if minGrid[0] is not None else 0, maxGrid[0] if maxGrid[0] is not None else 1000)
            yLimit = (minGrid[1] if minGrid[1] is not None else 0, maxGrid[1] if maxGrid[1] is not None else 1000)

            if textLength > (xLimit[1] * yLimit[1]):
                raise GridLayoutException
            else:

                rv = [xLimit[0], yLimit[0]]

                stopFlag = False

                while not stopFlag:
                    while rv[0] < xLimit[1]:
                        while rv[1] < yLimit[1]:
                            if rv[0]*rv[1] >= textLength:
                                stopFlag = True
                                break
                            else:
                                rv[1] +=1
                    
                        if not stopFlag:
                            rv[1] = yLimit[0]
                            rv[0] += 1
                        else:
                            break

                gridWidget.cols = rv[0]
                gridWidget.rows = rv[1] 

                dSizeX = gridWidget.size[0] / rv[0]
                dSizeY = gridWidget.size[1] / rv[1]

                currentCoordinates = [0, rv[1]-1]

                for i in range(textLength):

                    gridWidget.add_widget(GridLayout(size=(dSizeX, dSizeY), pos=(dSizeX * currentCoordinates[0] + gridWidget.pos[0], dSizeY * currentCoordinates[1] + gridWidget.pos[1])))

                    currentCoordinates[0] += 1
                    if currentCoordinates[0] >= rv[0]: 
                        currentCoordinates[1] -= 1
                        currentCoordinates[0] = 0

                return gridWidget

        def getCoordinates(coordinates, letter):

                if type(coordinates) == str:
                    coordinates = JSONFile(coordinates).get_value(letter)

                elif type(coordinates) == dict:
                    coordinates.get(letter)

                else:
                    raise TypeError

                return coordinates

        def putSymbol(self, letter, texture, widget):

            with widget.canvas.after:
                letterCoordinates = getCoordinates(coordinates, letter)
                exec(letterCoordinates)

        texture = getTexture(texture)
        widget = getGrid(widget, text, minGrid, maxGrid, separator)

        for i in range(len(text)):
            putSymbol(self, text[i], texture, widget.children[len(widget.children)-1-i])

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

    def loop(self, dt):
        
        self.threadLoopOverWrittenFlag = True

        self.screenManagerPassedFlag = False 

        while not self.screenManagerPassedFlag:
            try:
                self.showIntro()
                self.screenManagerPassedFlag = True
            except:
                pass

        self.engine.clock.schedule_once(self.pushPastIntro, -1)

