from gfx.py.appScreen import appScreen

from kivy.uix.scatterlayout import ScatterLayout

from gfx.py.Text import Text

class StartingScreen(appScreen):

    def load(self):

        self.name = 'Starting Screen'
        self.layout = ScatterLayout(size_hint=(1,1), pos_hint={"x": 0, "y": 0})
        #self.layout.appName = Text(engine=self.engine, size=(500, 200), pos=(35,65), text='!~ABCDEFG', maxGrid=(None, 3))
        #self.layout.appName = Text(engine=self.engine, text='0123456789~`!@"#№¤Ƀ$€£₽₴₪﷼₺₩￥₹元;%^:&?()_='+"{"+"}"+'[]\'|\<>*/-+,.ABCDEF', minSize=[16,9], maxSize=[160*2,90*2])
        self.layout.appName = Text(engine=self.engine, text='a@#H', maxSize=[320, 180], widgetPadding=[20,20,20,20], widgetSpacing=[20,20])

        self.layout.add_widget(self.layout.appName)
        self.add_widget(self.layout)

    def putText(self):
        
        self.layout.appName.show()
