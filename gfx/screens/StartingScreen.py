from ..appScreen import appScreen

from kivy.uix.stencilview import StencilView

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout

class StencilFloat(FloatLayout, StencilView):
    pass

class StartingScreen(appScreen):

    def load(self):

        self.name = 'Starting Screen'
        self.layout = RelativeLayout()

        self.layout.appName = StencilFloat(size_hint=(0.2,0.2), pos_hint={'x':0.4, 'y':0.8})
        
        self.layout.add_widget(self.layout.appName)
        self.add_widget(self.layout)
        
        #self.engine.clock.schedule_once(partial(self.engine.GUIThread.putText, self.engine, self.layout.appName, 'A'), 0)

        self.engine.GUIThread.putText(self.layout.appName, 'A')
