from engine.threadClass import threadClass

from kivy.core.audio import SoundLoader

import time

class playThread(threadClass):
    
    def loop(self, dt):

        self.threadLoopOverWrittenFlag = True
        self.playThreadStopFlag = True
        self.freezeAudioInsertFlag = False

        self.currentEndingIndex = self.engine.updateThread.i
        self.filenamesToPlayQueue = []

        self.copyFromMainThread()

        while True:
            if not self.threadStopFlag or not self.mainThread.threadStopFlag:
                self.executeAddons()

    def copyFromMainThread(self):
        
        if not hasattr(self, 'address'): self.address = self.mainThread.address
        if not hasattr(self, 'volume'): self.volume = self.mainThread.volume
        if not hasattr(self, 'extension'): self.extension = self.mainThread.extension
        if not hasattr(self, 'delay'): self.delay = self.mainThread.delay

    def getAudioObject(self):
        
        audioObject = SoundLoader.load((self.address if self.address not in self.name else "") + self.name + (self.extension if self.extension not in self.name else ""))
        audioObject.volume = self.volume

        return audioObject

    def getTime(self, addressString):
        
        if self.currentEndingIndex < self.engine.updateThread.i: self.currentEndingIndex = self.engine.updateThread.i
        
        dummySL = SoundLoader.load(addressString) #We not immediately loading audio file to play into our AudioObject as it may happen in different periods of time and also we intend to reuse it. Here, we use a dummy object to get a length of the file that hasn't been loaded yet. #TODO Change to a 3rd party module so we can save memory / processing tume, maybe? Remember about files extensions.
        dummySL.play()
        dummySL.volume = 0

        rv = (self.currentEndingIndex if self.engine.engineSettings.audioAppendOn == 'start' else self.engine.updateThread.i) + self.engine.updateThread.to('i', self.delay) + 1
        self.currentEndingIndex = rv + self.engine.updateThread.to('i', dummySL.length)

        dummySL.stop()

        print("TIME RV: ", str(rv))
        print("I: ", str(self.engine.updateThread.i))

        return rv 

    def addTask(self, filename):
        
        frame = self.getTime((self.address if self.address not in filename else "") + filename + (self.extension if self.extension not in filename else ""))
        instruction = 'self.engine.audioThread.threads[' + str(len(self.mainThread.threads)-1) +'].playAudio()'
        group = self.threadName + ' ' + (self.currentAddon.name if self.currentAddon is not None else '')

        self.engine.updateThread.addTask({"frame": frame, "task": instruction, "group": group})

    def addPlayQueue(self):

        for i in range(len(self.filenamesToPlayQueue)):
            self.addTask(self.filenamesToPlayQueue[i])

    def updatePlayQueue(self):
        
        if len(self.filenamesToPlayQueue) > 0:
            
            self.name = self.filenamesToPlayQueue[0]
            if len(self.filenamesToPlayQueue) > 1: self.filenamesToPlayQueue = self.filenamesToPlayQueue[1:]

    def insertAudio_s_IntoQueue(self, audios):
        
        if type(audios) != list: list(audios)

        while not self.freezeAudioInsertFlag:

            for audio in audios:

                self.freezeAudioInsertFlag = True
                self.filenamesToPlayQueue.append(audio)
                self.freezeAudioInsertFlag = False

            if self.engine.engineSettings.audioAppendOn == 'start':
                self.addPlayQueue()
            
            break

    def playAudio(self):

            self.updatePlayQueue()

            try:
                self.audioObject.unload()
            except:
                pass

            self.audioObject = self.getAudioObject()
            self.audioObject.play()
            
            if self.engine.engineSettings.audioAppendOn == 'end' and len(self.filenamesToPlayQueue) > 1:
                time.sleep(self.audioObject.length)
                self.addTask(self.filenamesToPlayQueue[1])

    def _pause(self):

        super()._pause()
        
        try:
            self.audioObject.pause()
        except:
            pass

    def _resume(self):
        
        super()._resume()
        self.audioObject.play()

    def _stop(self):
        
        super()._stop()
        
        self.filenamesToPlayQueue.clear()
        self.currentEndingIndex = self.engine.updateEngine.i

class audioThread(threadClass):

   
    def addThread_s_(self, threadNumber):
          
        if threadNumber is None:
            threadNumber = len(self.threads)

        while len(self.threads) <= threadNumber:
            newPlayThread = playThread(self.engine, mainThread=self, threadName='Audio Thread ' + str(len(self.threads)))
            self.threads.append(newPlayThread)

    def deleteThread_s_(self, threadNumber):

        for thread in self.threads[threadNumber:]:
            thread.stop() # TODO edit this function to deal not only with sound.

        self.threads = self.threads[:threadNumber]

    def loop(self, dt):
       
        self.waitForOtherThreads()

        while True:
            if not self.threadStopFlag:
                self.executeAddons()