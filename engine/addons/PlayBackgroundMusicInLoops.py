from engine.Addon import Addon

class PlayBackGroundMusicInLoops(Addon):

    def start(self):

        self.threadsConcernded = ['Audio']
        self.relatedFlags = {"Audio": [["playAllTracksFlag", [0, 0]]]}
        self._launch() 

    def stop(self):
        self._stop()

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
                    if ((getLastTrack() is not None) and (getLastTrack() != clearedShuffledOrder[0])) or len(clearedOrder) == 1:
                        rvPossible = True

            return clearedShuffledOrder
        
        if self.engine.audioThread.playAllTracksFlag[0]:
                    
            if (not hasattr(self.engine.audioThread, 'tracksOrder')) or (self.engine.appSettings.audioIfBeingPlayedTrackOrderRandomized == 'cycle'):
                self.engine.audioThread.tracksOrder = getTracksOrder(self.engine.audioThread.playAllTracksFlag[1])

            self.engine.updateThread.addTask({"task": "self.engine.audioThread.addThread_s_(0)", "group": 'Audio Thread 0 PlayBackgroundMusicInLoops'})
            self.engine.updateThread.addTask({"task": "self.engine.audioThread.threads[0].insertAudio_s_IntoQueue(self.engine.audioThread.tracksOrder)", "group": 'Audio Thread 0 PlayBackgroundMusicInLoops'})
            self.engine.updateThread.addTask({"task": 'self.engine.audioThread.threads[0]._start()', "group": 'Audio Thread 0 PlayBackgroundMusicInLoops'})

            while self.engine.updateThread.i < self.threads[0].currentEndingIndex: 
                pass