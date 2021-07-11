from kivy.core.audio import SoundLoader

import os
import random
import time

def audioThread(engine):

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
    
    while not engine.audioThread.stopFlag:

        order = getOrder()
        order = deleteProhibitedTracks(order, engine.settings.audioExcludedTracks)
        for index in order:
                playAudio(index, engine.settings.audioVolume)