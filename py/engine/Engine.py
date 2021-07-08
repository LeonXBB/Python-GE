from ..Settings import Settings as Settings

from py.engine.GUI import GUIThread as GUIThread
from py.engine.Audio import audioThread as audioThread
from py.engine.Input import inputThread as inputThread

from kivy.app import App

from kivy.clock import Clock

from kivy.uix.screenmanager import ScreenManager, NoTransition

import threading

class Engine(App): #settings, clock, screenManager, threads

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.settings = Settings()
        self.load_settings()

        self.clock = Clock

    def build(self, **kwargs):

        super().__init__(**kwargs)
        
        self.screenManager = ScreenManager(transition=NoTransition())
        return self.screenManager

    def start(self):

        self.GUIThread = threading.Timer(0.5, GUIThread, args=(self,))
        self.GUIThread.start()
        self.GUIThread.stopFlag = False

        self.audioThread = threading.Timer(0.5, audioThread, args=(self,))
        self.audioThread.daemon = True
        self.audioThread.start()
        self.audioThread.stopFlag = False

        self.controlsThread = threading.Timer(0.5, inputThread, args=(self,))
        self.controlsThread.daemon = True
        self.controlsThread.start()
        self.controlsThread.stopFlag = False

        self.timeThread = None
        self.internetThread = None

        self.run()

    def change_settings(self):
        pass

    def load_settings(self):
        self.settings.apply_values()

    def time_tick(self):
        pass