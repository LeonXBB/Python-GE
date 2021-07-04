from kivy.app import App

from kivy.clock import Clock
from functools import partial

from kivy.uix.screenmanager import ScreenManager, NoTransition

from gfx.screens.LoadingScreen import LoadingScreen as LoadingScreen
from gfx.screens.StartingScreen import StartingScreen as StartingScreen

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
        self.run()

    def change_settings(self):
        pass

    def load_settigns(self):
        pass

    def play_audio(self):
        pass

    def time_tick(self):
        pass