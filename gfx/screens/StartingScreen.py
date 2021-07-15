from ..appScreen import appScreen

from kivy.uix.stencilview import StencilView

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout

class StartingScreen(appScreen):

    def load(self):

        self.name = 'Starting Screen'
        self.layout = RelativeLayout()
        self.layout.appName = GridLayout(size=(100, 100), pos=(100,100))
        self.layout.add_widget(self.layout.appName)
        self.add_widget(self.layout)
           
    def putText(self):

        self.engine.GUIThread.putText(self.layout.appName, 'A!BCDEF')
