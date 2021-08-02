import multiprocessing

if __name__ == '__main__':

        from engine.Engine import Engine

        multiprocessing.freeze_support()
        appEngine = Engine()
        appEngine.initThreads()
        appEngine.start()