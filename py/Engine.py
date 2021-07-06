from kivy.app import App

from kivy.clock import Clock
from functools import partial

from kivy.uix.screenmanager import ScreenManager, NoTransition

from gfx.screens.LoadingScreen import LoadingScreen as LoadingScreen
from gfx.screens.StartingScreen import StartingScreen as StartingScreen

from kivy.core.audio import SoundLoader

import time
import os 
import random
import threading

class Engine(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.screenManager = ScreenManager()
        self.screenManager.add_widget(LoadingScreen())

        self.clock = Clock

    def build(self, **kwargs):

        super().__init__(**kwargs)
        return self.screenManager

    def start(self):

        def process_starting_screen(self, dt):
            
            self.screenManager.add_widget(StartingScreen())
            self.screenManager.current = 'Starting Screen'
        
        self.clock.schedule_once(partial(process_starting_screen, self), -1)
        
        audioThread = threading.Timer(0.5, self.manage_audio)
        audioThread.start()
        
        self.run()

    def change_settings(self):
        pass

    def load_settigns(self):
        pass

    def manage_audio(self):

        def get_order():

            for root, dirs, files in os.walk('audio'):
                audioFilesNumber = len(files)
            
            audioNumbersList = list(range(1, audioFilesNumber+1))
            random.shuffle(audioNumbersList)

            return audioNumbersList

        def play_audio(index):
            
            audioFile = SoundLoader.load('audio/' + str(index) + '.wav')
            audioFile.play()
            time.sleep(audioFile.length)

        order = get_order()
        for index in order:
            play_audio(index)

    def time_tick(self):
        pass