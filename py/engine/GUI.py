from functools import partial

from JSONFile import JSONFile

from gfx.screens.LoadingScreen import LoadingScreen as loadingScreen
from gfx.screens.StartingScreen import StartingScreen as startingScreen

def drawText(widget, text, texture='fontTexture', instructions=None, linesAmount=None, minSize=None):
    

    def getTexture(texture):
        
            if type(texture) == 'str':
                texture = JSONFile(texture)
            elif type(texture) == 'dict':
                pass

            return texture


    def getInstructions(instructions):
        pass 

    def getLinesAmount(linesAmount):
        pass

    def getMinSize(minSize):
        pass

    texture = getTexture(texture)

    with widget.canvas.after:
        pass


def showIntro(engine, dt):

    engine.screenManager.add_widget(startingScreen())
    engine.screenManager.current = 'Starting Screen'

def GUIThread(engine):
    
    engine.screenManager.add_widget(loadingScreen())
    engine.clock.schedule_once(partial(showIntro, engine), -1)