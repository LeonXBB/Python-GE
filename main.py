if __name__ == '__main__':

        import multiprocessing
        from engine.Engine import Engine

        with open('NEWIDEATEST.txt', 'w'): pass
        
        multiprocessing.freeze_support()
        appEngine = Engine()
        appEngine.initThreads()
        appEngine.start()