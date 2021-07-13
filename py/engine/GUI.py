from py.engine.threadClass import threadClass
from py.JSONFile import JSONFile

from functools import partial

from gfx.screens.LoadingScreen import LoadingScreen as loadingScreen
from gfx.screens.StartingScreen import StartingScreen as startingScreen

from kivy.uix.gridlayout import GridLayout

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

    def putText(self, widget, text, texture='fontTexture', coordinates='fontCoordinates', minGrid=(None, None), separator=' '):
        
        def getTexture(texture):
            
                if type(texture) == str:
                    texture = JSONFile(texture).get_all_values()
                
                elif type(texture) == dict:
                    pass

                else:
                    raise TypeError

                return texture

        def getGrid(widget, textLength, minGrid):
            
            #widget.grid = GridLayout()

            if minGrid[0] is not None and minGrid[1] is not None:
                if textLength <= minGrid[0] * minGrid[1]:
                    widget.cols = minGrid[0]
                    widget.rows = minGrid[1]
            
                else:
                    while textLength > minGrid[0] * minGrid[1]:
                        widget.cols += 1
                        widget.rows += 1

            elif (minGrid[0] is not None and minGrid[1] is None) or (minGrid[1] is not None and minGrid[0] is None):
                setAxis = ((minGrid[0], 'cols') if minGrid[1] is None else (minGrid[1]), 'rows')
                setattr(widget, setAxis[1], setAxis[0])
                setattr(widget, ('rows' if setAxis[1] == 'cols' else 'cols'), (textLength // setAxis[0] + (textLength % setAxis[0] > 0)))

            elif minGrid[0] is None and minGrid[1] is None:
                
                widget.cols = 0
                widget.rows = 0

                while textLength > widget.cols * widget.rows:
                    widget.cols += 1
                    widget.rows += 1

            for i in range(widget.cols * widget.rows):
                widget.add_widget(GridLayout())

            #widget.add_widget(widget.grid)

            return widget

        def getCoordinates(coordinates, letter):

                if type(coordinates) == str:
                    coordinates = JSONFile(coordinates).get_value(letter)

                elif type(coordinates) == dict:
                    coordinates.get(letter)

                else:
                    raise TypeError

                return coordinates

        def putLetter(self, letter, texture, widget, dt):

            with widget.canvas.after:
                letterCoordinates = getCoordinates(coordinates, letter)
                exec(letterCoordinates)

        texture = getTexture(texture)
        widget = getGrid(widget, len(text), minGrid)

        print(widget.pos, widget.size)

        for i in range(len(text)):
            self.engine.clock.schedule_once(partial(putLetter, self, text[i], texture, widget.children[i]),0)
      
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

