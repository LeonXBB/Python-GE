from py.engine.threadClass import threadClass
from py.JSONFile import JSONFile

from functools import partial

from gfx.screens.LoadingScreen import LoadingScreen as loadingScreen
from gfx.screens.StartingScreen import StartingScreen as startingScreen

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from kivy.graphics import *

class GUIThread(threadClass):
    
    def switchCoordinates(self, values, systemIn, systemOut, relative=False, relativity=None):

        # pixels, (geographical) coordinates, percentage

        if systemIn == 'pixels':
            
            if not relative:

                dx = self.engine.settings.windowWidth / 100
                dy = self.engine.settings.windowHeight / 100

                percentX = values[0] / dx
                percentY = values[1] / dy 

                midValues = [percentX, percentY]
            
            elif relative:
                pass

        elif systemIn == 'coordinates':
            pass

        elif systemIn == 'percentage':
            
            if not relative:
                midValues = [values[0], values[1]]

            elif relative:
                pass

        if systemOut == 'pixels':
            
            if not relative:
            
                dx = self.engine.settings.windowWidth / 100
                dy = self.engine.settings.windowHeight / 100
            
                pixelX = midValues[0] * dx
                pixelY = midValues[1] * dy

                rv = (pixelX, pixelY)

            elif relative:
                pass

        elif systemOut == 'coordinates':
            pass

        elif systemOut == 'percentage':
            
            if not relative:
                rv = (midValues[0], midValues[1])
            elif relative:
                pass

        print(rv)

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
            
            widget.grid = GridLayout()

            if minGrid[0] is not None and minGrid[1] is not None:
                if textLength <= minGrid[0] * minGrid[1]:
                    widget.grid.cols = minGrid[0]
                    widget.grid.rows = minGrid[1]
            
                else:
                    while textLength > minGrid[0] * minGrid[1]:
                        widget.grid.cols += 1
                        widget.grid.rows += 1

            elif (minGrid[0] is not None and minGrid[1] is None) or (minGrid[1] is not None and minGrid[0] is None):
                setAxis = ((minGrid[0], 'cols') if minGrid[1] is None else (minGrid[1]), 'rows')
                setattr(widget.grid, setAxis[1], setAxis[0])
                setattr(widget.grid, ('rows' if setAxis[1] == 'cols' else 'cols'), (textLength // setAxis[0] + (textLength % setAxis[0] > 0)))

            elif minGrid[0] is None and minGrid[1] is None:
                
                widget.grid.cols = 0
                widget.grid.rows = 0

                while textLength > widget.grid.cols * widget.grid.rows:
                    widget.grid.cols += 1
                    widget.grid.rows += 1

            widget.add_widget(widget.grid)

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

            subWidget = Label()
            widget.add_widget(subWidget)
            with subWidget.canvas.after:
                letterCoordinates = getCoordinates(coordinates, letter)
                exec(letterCoordinates)

        texture = getTexture(texture)
        widget = getGrid(widget, len(text), minGrid)

        for letter in text:
            self.engine.clock.schedule_once(partial(putLetter, self, letter, texture, widget),1)

    def pushPastIntro(self, dt):

        sS = startingScreen(self.engine)
        sS.load()
        self.engine.screenManager.add_widget(sS)
        self.engine.screenManager.current = 'Starting Screen'

    def showIntro(self):

        lS = loadingScreen(self.engine)
        lS.load()
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

