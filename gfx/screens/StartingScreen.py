from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen

from kivy.uix.label import Label

class StartingScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.name = 'Starting Screen'

        self.layout = FloatLayout()

        self.layout.appNameLabel = Label(text='AIRWORDS', pos=(40,115))

        self.layout.add_widget(self.layout.appNameLabel)

        self.add_widget(self.layout)