from ..Settings import Settings as Settings

from engine.core.GUI import GUIThread as GUIThread
from engine.core.Audio import audioThread as audioThread
from engine.core.Controls import controlsThread as controlsThread

from kivy.app import App

from kivy.clock import Clock

from kivy.uix.screenmanager import ScreenManager, NoTransition

import threading

class Engine(App): #settings, clock, screenManager, threads

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.screenManager = None

        self.settings = Settings()
        self.load_settings()

        self.clock = Clock

        self.GUIThread = GUIThread(self)
        self.audioThread = audioThread(self)
        self.controlsThread = controlsThread(self)

        self.timeThread = threading.Timer(0.5, self.threadPass, args=(self,))
        self.internetThread = threading.Timer(0.5, self.threadPass, args=(self,))

        self.threads = [self.GUIThread, self.audioThread, self.controlsThread, self.timeThread, self.internetThread]

    def build(self, **kwargs):

        super().__init__(**kwargs)

        self.screenManager = ScreenManager(transition=NoTransition())
        return self.screenManager

    def threadPass(self, engine):
        pass

    def start(self):

        for thread in self.threads:
            thread.start()

        self.run()

    def change_settings(self):
        pass

    def load_settings(self):
        self.settings.apply_values()

    def time_tick(self):
        pass