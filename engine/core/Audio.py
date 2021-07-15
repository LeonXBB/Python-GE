from engine.threadClass import threadClass

from kivy.core.audio import SoundLoader

import os
import random
import time

class audioThread(threadClass):

    def loop(self, dt):

        def getOrder():

            for root, dirs, files in os.walk('audio'):
                audioFilesNumber = len(files)
                    
            audioNumbersList = list(range(1, audioFilesNumber+1))

            return audioNumbersList

        def deleteProhibitedTracks(order, excluded_tracks):
            
            rv = list(set(order).symmetric_difference(set(excluded_tracks)))            
            random.shuffle(rv)
            return rv

        def playAudio(index, volume):
            
            audioFile = SoundLoader.load('audio/' + str(index) + '.wav')
            audioFile.volume = volume
            audioFile.play()
            if audioFile.length > 0: time.sleep(audioFile.length)
        
        self.threadLoopOverWrittenFlag = True

        while not self.engine.audioThread.threadStopFlag:

            order = getOrder()
            order = deleteProhibitedTracks(order, self.engine.settings.audioExcludedTracks)
            for index in order:
                    playAudio(index, self.engine.settings.audioVolume)