from gfx.py.appScreen import appScreen

from kivy.uix.scatterlayout import ScatterLayout

from gfx.py.Text import Text

class StartingScreen(appScreen):

    def load(self):

        self.name = 'Starting Screen'
        self.layout = ScatterLayout(size_hint=(1,1), pos_hint={"x": 0, "y": 0})
        #self.layout.appName = Text(engine=self.engine, size=(500, 200), pos=(35,65), text='!~ABCDEFG', maxGrid=(None, 3))
        self.layout.appName = Text(engine=self.engine, size=(1800, 900), text='012345`~!|\*/-+,.', maxSize=[400, 150], padding=[50], spacing=[20])

        self.layout.add_widget(self.layout.appName)
        self.add_widget(self.layout)

    def putText(self):
        
        self.layout.appName.show()
