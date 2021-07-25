from engine.threadClass import threadClass

from kivy.core.audio import SoundLoader

import os
import random
import time

class playThread(threadClass):
    
    def loop(self, dt):

        self.threadLoopOverWrittenFlag = True
        self.playThreadStopFlag = True
        self.freezeAudioInsertFlag = False

        self.currentEndingIndex = self.engine.updateThread.i
        self.filenamesToPlayQueue = []

        self.copyFromMainThread()

        self.audioObject = self.getAudioObject()

        while True:
            if not self.threadStopFlag:
                pass

    def copyFromMainThread(self):
        
        if not hasattr(self, 'address'): self.address = self.mainThread.address
        if not hasattr(self, 'volume'): self.volume = self.mainThread.volume
        if not hasattr(self, 'extension'): self.extension = self.mainThread.extension
        if not hasattr(self, 'delay'): self.delay = self.mainThread.delay

    def getAudioObject(self):
        audioObject = SoundLoader
        return audioObject

    def insertAudio_s_IntoQueue(self, audios):
        
        if type(audios) != list: list(audios)

        for audio in audios:

            while not self.freezeAudioInsertFlag:

                self.freezeAudioInsertFlag = True

                self.filenamesToPlayQueue.append(audio)
                
                self.freezeAudioInsertFlag = False

    def getTime(self, addressString):
        
        if self.currentEndingIndex < self.engine.updateThread.i: self.currentEndingIndex = self.engine.updateThread.i
        
        dummySL = SoundLoader #We not immediately loading audio file to play into our AudioObject as it may happen in different periods of time and also we intend to reuse it. Here, we use a dummy object to get a length of the file that hasn't been loaded yet. #TODO Change to a 3rd party module so we can save memory / processing tume, maybe? Remember about files extensions.
        dummySL.load(addressString)

        rv = (self.currentEndingIndex if self.engine.engineSettings.audioAppendOn == 'start' else self.engine.updateThread.i) + self.engine.updateThread.to('i', self.delay)
        self.currentEndingIndex = rv + self.engine.updateThread.to('i', dummySL.length)

        return rv 

    def addTask(self, filename):
        
        time = self.getTime((self.address if self.address not in filename else "") + filename + (self.extension if self.extension not in filename else ""))
        instruction = 'self.engine.audioThread.threads[' + self.selfIndex +'].playThreadStopFlag = False'
        group = self.threadName

        self.engine.updateThread.addTask({"time": time,"task": instruction, "group": group})

    def play(self):

        if len(self.filenamesToPlayQueue) > 0:
            
            self.name = self.filenamesToPlayQueue[0]
            if len(self.filenamesToPlayQueue) > 1: self.filenamesToPlayQueue = self.filenamesToPlayQueue[1:]

            try:
                self.audioObject.unload()
            except:
                pass

            self.audioObject.load((self.address if self.address not in self.name else "") + self.name + (self.extension if self.extension not in self.name else ""))
            self.audioObject.volume = self.volume

            self.audioObject.play()
            
            if self.engine.engineSettings.audioAppendOn == 'end' and len(self.filenamesToPlayQueue) > 1:
                time.sleep(self.audioObject.length)
                self.addTask(self.filenamesToPlayQueue[1])

    def _start(self):

        super()._start()

        for i in range(1 if self.engine.engineSettings.audioAppendOn == 'end' else len(self.filenamesToPlayQueue)):
            self.addTask(self.filenamesToPlayQueue[i])

    def _pause(self):

        super()._pause()
        self.audioObject.pause()

    def _resume(self):
        
        super()._resume()
        self.audioObject.play()

    def _stop(self):
        
        super()._stop()
        
        self.filenamesToPlayQueue.clear()
        self.currentEndingIndex = self.engine.updateEngine.i

class audioThread(threadClass):

    def addThread_s_(self, threadsNumber):
          
        if threadsNumber is None:
            threadsNumber = len(self.threads)

        while len(self.threads) <= threadsNumber:
            newPlayThread = playThread(self.engine, mainThread=self, threadName='Audio Thread ' + str(len(self.threads)))
            newPlayThread.start()
            self.threads.append(newPlayThread)

    def deleteThread_s_(self, threadsNumber):

        for thread in self.threads[threadsNumber:]:
            thread.stop() # TODO edit this function to deal not only with sound.

        self.threads = self.threads[:threadsNumber]

    def getTracksOrder(self, randomly):

        def getAudioNumbersList(self):

            for root, dirs, files in os.walk(self.address):
                audioFilesNumber = len(files)
                
                audioNumbersList = list(range(1, audioFilesNumber+1))

            return audioNumbersList

        def deleteProhibitedTracks(self, nonClearedOrder):
            return list(set(nonClearedOrder).symmetric_difference(set(self.excludedTracks)))            
            
        def randomlyShuffle(self, clearedOrder, i):
            
            for i in range(i):
                random.shuffle(clearedOrder)
            
            return clearedOrder

        nonClearedOrder = getAudioNumbersList(self) 
        clearedOrder = deleteProhibitedTracks(self, nonClearedOrder)
        clearedShuffledOrder = (randomlyShuffle(self, clearedOrder, random.randint(1,10)) if randomly else clearedOrder)

        return clearedShuffledOrder

    def loop(self, dt):
       
        self.threadLoopOverWrittenFlag = True

        self.playAllTracksFlag = [False, False]

        while True:
            if not self.threadStopFlag:

                if self.playAllTracksFlag[0]:
                    
                    if (self.tracksOrder is None) or ((self.tracksOrder is not None) and (self.engine.appSettings.audioIfBeingPlayedTrackOrderRandomized == 'cycle')): 
                        
                        lastTrack = None

                        if not self.engine.appSettings.audioAllowTrackRepeatAtCycleEndStart and self.tracksOrder is not None: lastTrack = self.tracksOrder[-1] 
                        self.tracksOrder = self.getTracksOrder(self.playAllTracksFlag[1])
                        while len(self.tracksOrder) > 1 and lastTrack is not None and self.tracksOrder[0] == lastTrack:
                            self.tracksOrder = self.getTracksOrder(self.playAllTracksFlag[1])

                    self.addThread_s_(0)
                    self.threads[0].insertAudio_s_IntoQueue(self.tracksOrder)
                    print('here')
                    self.engine.updateThread.addTask({"task": 'self.engine.audioThread.threads[0]._start()', "group": 'Audio Thread 0'})

                    while self.engine.updateThread.i < self.threads[0].currentEndingIndex: 
                        pass 