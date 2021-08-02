from kivy.app import App

from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, NoTransition

class Window(App):

    '''def __reduce__(self):
        return (self.__class__, ())

    def __getstate__(self):
        print("FINALLY")
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):      
        self.__dict__.update(state)''' 

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.clock = Clock
        self.screenManager = ScreenManager(transition=NoTransition())

    def build(self):       
        super().__init__()
        return self.screenManager