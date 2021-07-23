from sys import flags
from engine.threadClass import threadClass

from kivy.core.audio import SoundLoader

import os
import random
import time

class audioThread(threadClass):

    def getTracksOrder(self, randomly):

        def getAudioNumbersList(self):

            for root, dirs, files in os.walk(self.address):
                audioFilesNumber = len(files)
                
                audioNumbersList = list(range(1, audioFilesNumber+1))

            return audioNumbersList

        def deleteProhibitedTracks(self, nonClearedOrder):
            return list(set(nonClearedOrder).symmetric_difference(set(self.excluded_tracks)))            
            
        def randomlyShuffle(self, clearedOrder, i):
            
            for i in range(i):
                random.shuffle(clearedOrder)
            
            return clearedOrder

        nonClearedOrder = getAudioNumbersList(self) 
        clearedOrder = deleteProhibitedTracks(self, nonClearedOrder)
        clearedShuffledOrder = (randomlyShuffle(self, clearedOrder, random.randint(1,10)) if randomly else clearedOrder)

        return clearedShuffledOrder

    def playAudio(self, name, **kwargs): # to be used when someone/something needs to output an audiofile, not by updateThread (it calls kivy's method directly)
        
        if kwargs.get('address') is None: address = self.address
        if kwargs.get('volume') is None: volume = str(self.volume)
        if kwargs.get('extension') is None: extension = self.extension
        if kwargs.get('delay') is None: delay = 0
        if kwargs.get('parallel') is None: parallel = False

        audioFile = SoundLoader.load(address + name + (extension if extension not in name else ""))
        audioFile.volume = volume

        if not self.freezeAudioIndexesFlag: # TODO we can skip reuploading each file everytime by uploading them once (at the start / on the go) and reusing them. Look into it. (Gotta add more parameters to self.audios entry than just audiofile)
            self.freezeAudioIndexesFlag = True
            self.audios.append(audioFile)
            index = len(self.audios)
            self.freezeAudioIndexesFlag = False

        playtime = self.engine.updateThread.i + 1 + delay + (0 if parallel else self.endTimeMark)
        instruction = 'self.engine.audioThread.audios[' + str(index) + '].play()'

        self.engine.updateThread.addTask([playtime,instruction])

        self.endTimeMark = max(self.endTimeMark, playtime + self.audios[index].length)

    def loop(self, dt):
       
        self.threadLoopOverWrittenFlag = True

        self.playAllTracksFlag = [False, False]
        self.freezeAudioIndexesFlag = False

        while True:
            if not self.threadStopFlag:

                if self.playAllTracksFlag[0]:
                    
                    tracksOrder = self.getTracksOrder(self.playAllTracksFlag[1])
                   
                    for index in tracksOrder:
                        self.playAudio(str(index))