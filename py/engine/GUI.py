from py.engine.threadClass import threadClass
from py.JSONFile import JSONFile

from functools import partial

from gfx.screens.LoadingScreen import LoadingScreen as loadingScreen
from gfx.screens.StartingScreen import StartingScreen as startingScreen

from kivy.uix.gridlayout import GridLayout

from kivy.graphics import *

class GUIThread(threadClass):
    
    def drawText(self, widget, text, texture='fontTexture', instructions='fontInstructions', minGrid=(None, None), separator=' '):
        
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

        def getInstruction(instructions, letter):

                if type(instructions) == str:
                    instructions = JSONFile(instructions).get_value(letter)

                elif type(instructions) == dict:
                    instructions.get(letter)

                else:
                    raise TypeError

                return instructions

        texture = getTexture(texture)
        widget = getGrid(widget, len(text), minGrid)
        
        for letter in text:
            subWidget = GridLayout()
            widget.add_widget(subWidget)
            with subWidget.canvas.before:
                letterInstruction = getInstruction(instructions, letter)
                #self.engine.clock.schedule_once(partial(exec, (letterInstruction), 0))
                exec(letterInstruction)

    def showIntro(self, dt):

        import time 
        time.sleep(5)

        sS = startingScreen(self.engine)
        sS.load()
        self.engine.screenManager.add_widget(sS)
        self.engine.screenManager.current = 'Starting Screen'

    def loop(self, dt):
        
        self.threadLoopOverWritenFlag = True

        self.screenManagerPassedFlag = False 

        while not self.screenManagerPassedFlag:
            try:
                lS = loadingScreen(self.engine)
                lS.load()
                self.engine.screenManager.add_widget(lS)
                self.engine.screenManager.current = 'Loading Screen'
                self.screenManagerPassedFlag = True
            except:
                pass

        self.engine.clock.schedule_once(self.showIntro, -1)

