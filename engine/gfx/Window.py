from kivy.app import App

from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, NoTransition

class Window(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.clock = Clock
        self.screenManager = ScreenManager(transition=NoTransition())

    def build(self):       
        super().__init__()
        return self.screenManager