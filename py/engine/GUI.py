from functools import partial

from gfx.screens.LoadingScreen import LoadingScreen as loadingScreen
from gfx.screens.StartingScreen import StartingScreen as startingScreen

def drawText(widget, text, texture):
    pass

def showIntro(engine, dt):

    engine.screenManager.add_widget(startingScreen())
    engine.screenManager.current = 'Starting Screen'

def GUIThread(engine):
    
    engine.screenManager.add_widget(loadingScreen())
    engine.clock.schedule_once(partial(showIntro, engine), -1)