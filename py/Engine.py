from re import I
from kivy.app import App

from kivy.uix.screenmanager import ScreenManager

from gfx.screens.LoadingScreen import LoadingScreen as LoadingScreen
from gfx.screens.StartingScreen import StartingScreen as StartingScreen


class Engine(App):

    def build(self, **kwargs):

        super().__init__(**kwargs)
        self.screenManager = ScreenManager()
        self.screenManager.add_widget(LoadingScreen(name='Loading Screen'))
        return self.screenManager

    def start(self):

        def process_starting_screen(self):
            
            self.screenManager.add_widget(StartingScreen(name='Starting Screen'))
            self.screenManager.current = 'Starting Screen'

        self.run()
        process_starting_screen(self)
        return self

    def change_settings(self):
        pass

    def load_settigns(self):
        pass

    def play_audio(self):
        pass

    def time_tick(self):
        pass