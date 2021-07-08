from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen

from kivy.uix.label import Label

class StartingScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.name = 'Starting Screen'

        self.layout = FloatLayout()

        self.layout.appNameLabel = Label(text='AIRWORDS', size_hint=(.2, .2), pos_hint={'center_x':0.5, 'center_y':0.8})

        self.layout.add_widget(self.layout.appNameLabel)

        self.add_widget(self.layout)