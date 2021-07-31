from engine.Addon import Addon

class PlayBackgroundMusicInLoops(Addon):

    def __init__(self, engine, name):

        super().__init__(engine, name)
        
        self.threadsConcerned = ['Audio']
        self.relatedFlags = {"Audio": [["playAllTracksFlag", True]]}
        self.autostart = False
        self.parameters = {"randomly": True, "tracksOrder": [], "lastTrack": None}

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
                return self.parameters.get('lastTrack')

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
        
        if self.engine.audioThread.playAllTracksFlag:

            if (len(self.engine.audioThread.threads) == 0) or (len(self.engine.audioThread.threads) > 0 and self.engine.audioThread.threads[0].currentEndingIndex <= self.engine.updateThread.i):
                if (len(self.parameters.get('tracksOrder')) == 0) or (self.engine.appSettings.audioIfBeingPlayedTrackOrderRandomized == 'cycle'):
                    self.parameters["tracksOrder"] = getTracksOrder(self, self.parameters.get('randomly'))
                self.parameters['lastTrack'] = self.parameters.get('tracksOrder')[-1]
                print("I: ", str(self.engine.updateThread.i))
                self.engine.updateThread.addTask({"task": "self.engine.audioThread.addThread_s_(0)", "group": 'Audio Thread 0 PlayBackgroundMusicInLoops'})
                print("I: ", str(self.engine.updateThread.i))
                self.engine.updateThread.addTask({"task": "if not self.engine.audioThread.threads[0].is_alive(): self.engine.audioThread.threads[0].start()", "group": 'Audio Thread 0 PlayBackgroundMusicInLoops'})
                print("I: ", str(self.engine.updateThread.i))
                self.engine.updateThread.addTask({"task": 'self.engine.audioThread.threads[0].insertAudio_s_IntoQueue([str(i) for i in self.engine.loadedAddons.get("PlayBackgroundMusicInLoops").parameters.get("tracksOrder")])', "group": 'Audio Thread 0 PlayBackgroundMusicInLoops'})
                print("I: ", str(self.engine.updateThread.i))
                #self.engine.updateThread.addTask({"frame": "self.engine.audioThread.threads[0].currentEndingIndex", "task": "self.engine.loadedAddons.get('PlayBackgroundMusicInLoops').start()", "group": "ShowIntro"})
                #self.autostart = True