from py.Settings import Settings as Settings
from py.Engine import Engine as Engine

if __name__ == '__main__':

    appSettings = Settings()
    appSettings.apply_values()

    appEngine = Engine()
    appEngine.start()