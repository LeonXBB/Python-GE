from kivy.uix.screenmanager import Screen

from kivy.uix.label import Label

class StartingScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.name = 'Starting Screen'
        self.add_widget(Label(text="THIS IS A STARTING SCREEN"))