from functools import partial

from py.JSONFile import JSONFile

from gfx.screens.LoadingScreen import LoadingScreen as loadingScreen
from gfx.screens.StartingScreen import StartingScreen as startingScreen

from kivy.uix.gridlayout import GridLayout

from kivy.graphics import Line

def drawText(widget, text, texture='fontTexture', instructions='fontInstructions', minGrid=(None, None)):
    
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
    
    print(widget.grid.__dict__)
    '''for subWidget in widget.grid.widgets:
        with subWidget.canvas.before:
            for letter in text:
                letterInstruction = getInstruction(instructions, letter)
                exec(letterInstruction + ')')'''


def showIntro(engine, dt):

    engine.screenManager.add_widget(startingScreen())
    engine.screenManager.current = 'Starting Screen'

def GUIThread(engine):
    
    engine.screenManager.add_widget(loadingScreen())
    engine.screenManager.current = 'Loading Screen'

    engine.clock.schedule_once(partial(showIntro, engine), -1)