from kivy.uix.screenmanager import Screen

class appScreen(Screen):

    def __init__(self, engine, **kwargs):

        super().__init__(**kwargs)

        self.engine = engine