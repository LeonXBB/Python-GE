from ..appScreen import appScreen

from kivy.uix.stencilview import StencilView

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout

class StartingScreen(appScreen):

    def load(self):

        self.name = 'Starting Screen'
        self.layout = RelativeLayout()
        self.layout.appName = GridLayout(size=(self.engine.settings.windowWidth / 5, self.engine.settings.windowHeight / 5), pos=(self.engine.settings.windowWidth / 5 * 2, self.engine.settings.windowHeight / 5 * 4))
        self.layout.add_widget(self.layout.appName)
        self.add_widget(self.layout)
           
    def putText(self):

        self.engine.GUIThread.putText(self.layout.appName, 'ABCDEF')
