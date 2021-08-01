import multiprocessing

from engine.Engine import Engine as Engine

if __name__ == '__main__':
    multiprocessing.freeze_support()
    appEngine = Engine()
    appEngine.start()