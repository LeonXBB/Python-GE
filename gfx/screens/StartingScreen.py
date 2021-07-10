from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen

from kivy.uix.label import Label

from py.engine.GUI import drawText

class StartingScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.name = 'Starting Screen'

        self.layout = FloatLayout()

        self.layout.appName = FloatLayout(size_hint=(.2, .2), pos_hint={'center_x':0.5, 'center_y':0.8})
        drawText(self.layout.appName, 'AAAAAAAAAAAAAAAAAAAA')

        self.layout.add_widget(self.layout.appName)

        self.add_widget(self.layout)