from py.Settings import Settings as Settings
from py.Engine import Engine as Engine
from kivy.config import Config

if __name__ == '__main__':

    appSettings = Settings()
    app
    Config.set('graphics', 'fullscren', appSettings.windowFullscreen)
    Config.set('graphics', 'resizable', False)
    Config.set('graphics', 'width', appSettings.windowWidth)
    Config.set('graphics', 'height', appSettings.windowHeight)

    appEngine = Engine()
    appEngine.start()