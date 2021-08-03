import multiprocessing
from engine.Engine import Engine

if __name__ == '__main__':

        multiprocessing.freeze_support()
        appEngine = Engine()
        appEngine.initThreads()
        appEngine.start()