from ..appScreen import appScreen

from kivy.uix.floatlayout import FloatLayout

class StartingScreen(appScreen):

    def load(self):

        self.name = 'Starting Screen'
        self.layout = FloatLayout()

        self.layout.appName = FloatLayout(size_hint=(.2, .2), pos_hint={'center_x':0.5, 'center_y':0.8})
        self.engine.GUIThread.putText(self.layout.appName, 'A')

        self.layout.add_widget(self.layout.appName)
        self.add_widget(self.layout)