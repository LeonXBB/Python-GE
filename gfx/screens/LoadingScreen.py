from kivy.uix.screenmanager import Screen

from kivy.uix.label import Label

class LoadingScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.name = 'Loading Screen'
        self.add_widget(Label(text="FOR DEVELOPING PURPOSES ONLY"))
