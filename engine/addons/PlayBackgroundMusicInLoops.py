from engine.Addon import Addon

class PlayBackgroundMusicInLoops(Addon):

    def __init__(self, engine, name):

        super().__init__(engine, name)
        
        self.threadsConcerned = ['Audio']
        self.relatedFlags = {"Audio": [["playAllTracksFlag", True]]}
        self.autostart = False
        self.parameters = {"Randomly": True}

    def start(self):
        self._launch() 

    def stop(self):
        self._stop()

    def pause(self):
        self._pause()

    def resume(self):
        self._resume()

    def func(self):

        import random
        import os

        def getTracksOrder(self, randomly):

            rvPossible = False

            def getLastTrack(self):
                
                if hasattr(self.engine.audioThread, "tracksOrder"):
                    return self.engine.audioThread.tracksOrder
                else:
                    return None 

            def getAudioNumbersList(self):

                for root, dirs, files in os.walk(self.engine.audioThread.address):
                    audioFilesNumber = len(files)
                
                audioNumbersList = list(range(1, audioFilesNumber+1))

                return audioNumbersList

            def deleteProhibitedTracks(self, nonClearedOrder):
                return list(set(nonClearedOrder).symmetric_difference(set(self.engine.audioThread.excludedTracks)))            
                
            def randomlyShuffle(self, clearedOrder, i):
                
                for i in range(i):
                    random.shuffle(clearedOrder)
                
                return clearedOrder

            while not rvPossible:

                nonClearedOrder = getAudioNumbersList(self) 
                clearedOrder = deleteProhibitedTracks(self, nonClearedOrder)
                clearedShuffledOrder = (randomlyShuffle(self, clearedOrder, random.randint(1,10)) if randomly else clearedOrder)

                if not self.engine.appSettings.audioAllowTrackRepeatAtCycleEndStart:
                    if ((getLastTrack(self) is not None) and (getLastTrack(self) != clearedShuffledOrder[0])) or len(clearedOrder) == 1 or (getLastTrack(self) is None):
                        rvPossible = True

            return clearedShuffledOrder
        
        while self.engine.audioThread.playAllTracksFlag:
            
            self.resume() #TODO add if statement
            
            if (not hasattr(self.engine.audioThread, 'tracksOrder')) or (self.engine.appSettings.audioIfBeingPlayedTrackOrderRandomized == 'cycle'):
                self.engine.audioThread.tracksOrder = getTracksOrder(self, self.parameters.get('Randomly'))

            self.engine.updateThread.addTask({"frame": "next", "task": "self.engine.audioThread.addThread_s_(0)", "group": 'Audio Thread 0 PlayBackgroundMusicInLoops'})
            self.engine.updateThread.addTask({"frame": "next", "task": "self.engine.audioThread.threads[0].start()", "group": 'Audio Thread 0 PlayBackgroundMusicInLoops'})
            self.engine.updateThread.addTask({"frame": "next", "task": 'self.engine.audioThread.threads[0].insertAudio_s_IntoQueue([str(i) for i in self.engine.audioThread.tracksOrder])', "group": 'Audio Thread 0 PlayBackgroundMusicInLoops'})

            '''while self.engine.updateThread.i < self.engine.audioThread.threads[0].currentEndingIndex: 
                self.pause()
            '''
            self.engine.audioThread.playAllTracksFlag = False #TODO think something about repeat