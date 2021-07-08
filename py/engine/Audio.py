from kivy.core.audio import SoundLoader

import os
import random
import time

def audioThread(engine):

    def get_order():

        for root, dirs, files in os.walk('audio'):
            audioFilesNumber = len(files)
                
        audioNumbersList = list(range(1, audioFilesNumber+1))

        return audioNumbersList

    def delete_prohibited_tracks(order, excluded_tracks):
        
        rv = list(set(order).symmetric_difference(set(excluded_tracks)))            
        random.shuffle(rv)
        return rv

    def play_audio(index, volume):
        
        audioFile = SoundLoader.load('audio/' + str(index) + '.wav')
        audioFile.volume = volume
        audioFile.play()
        time.sleep(audioFile.length)
    
    while not engine.audioThread.stopFlag:

        order = get_order()
        order = delete_prohibited_tracks(order, engine.settings.audioExcludedTracks)
        for index in order:
                play_audio(index, engine.settings.audioVolume)