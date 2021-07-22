from engine.gfx.py.root.appScreen import appScreen

from kivy.uix.label import Label

class LoadingScreen(appScreen):

    def load(self):

        self.name = 'Loading Screen'
        
        self.add_widget(Label(text="FOR DEVELOPING PURPOSES ONLY"))
