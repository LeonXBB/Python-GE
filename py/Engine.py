from py.Settings import Settings as Settings

from kivy.app import App

from kivy.clock import Clock
from functools import partial

from kivy.uix.screenmanager import ScreenManager, NoTransition

from gfx.screens.LoadingScreen import LoadingScreen as loadingScreen
from gfx.screens.StartingScreen import StartingScreen as startingScreen

from pynput import keyboard

from kivy.core.audio import SoundLoader

import time
import os 
import sys
import random
import threading

class Engine(App): #settings, clock, screenManager, audioThread, GUIThread

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.settings = Settings()
        self.load_settings()

        self.clock = Clock

    def build(self, **kwargs):

        def processStartingScreen(self, dt):
            
            self.screenManager.add_widget(startingScreen())
            self.screenManager.current = 'Starting Screen'

        super().__init__(**kwargs)
        
        self.screenManager = ScreenManager()
        self.screenManager.add_widget(loadingScreen())
        self.clock.schedule_once(partial(processStartingScreen, self), -1)

        return self.screenManager

    def start(self):

        self.audioThread = threading.Timer(0.5, self.manage_audio)
        self.audioThread.start()
        
        self.GUIThread = threading.Timer(0.1, self.run)
        self.GUIThread.start()

        self.userControlsThread = threading.Timer(0.1, self.getInput)
        self.userControlsThread.start()

    def getInput(self):
        
        global threads 
        threads = [self.audioThread, self.userControlsThread, self.GUIThread]

        def on_press(key):
            pass

        def on_release(key):

            if key == keyboard.Key.esc:
                for thread in threads: thread.cancel()
                sys.exit()

        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener: 
            listener.join()

    def change_settings(self):
        pass

    def load_settings(self):
        self.settings.apply_values()

    def manage_audio(self):

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

        while True:
            order = get_order()
            order = delete_prohibited_tracks(order, self.settings.audioExcludedTracks)
            for index in order:
                play_audio(index, self.settings.audioVolume)

    def time_tick(self):
        pass