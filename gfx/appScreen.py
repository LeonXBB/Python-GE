from kivy.uix.screenmanager import Screen

class appScreen(Screen):

    def __init__(self, engine, autoLaunch=False, **kwargs):

        super().__init__(**kwargs)

        self.engine = engine

        if autoLaunch:

            self.load()
            self.putText()

    def load(self):
        pass

    def putText(self):
        pass