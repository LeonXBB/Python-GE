from gfx.py.appScreen import appScreen

from kivy.uix.gridlayout import GridLayout
from kivy.uix.scatterlayout import ScatterLayout

from gfx.py.Text import Text

class StartingScreen(appScreen):

    def load(self):

        self.name = 'Starting Screen'
        self.layout = ScatterLayout(size_hint=(1,1), pos_hint={"x": 0, "y": 0})
        self.layout.appName = GridLayout(size=(500, 200), pos=((self.engine.settings.windowWidth / 10)*2.9, (self.engine.settings.windowHeight / 10)*7))
        
        self.layout.add_widget(self.layout.appName)
        self.add_widget(self.layout)

    def putText(self):
        
        Text(self.engine, self.layout.appName, 'ABCDEF', maxGrid=(None, 2)).show()
