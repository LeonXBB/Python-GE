from kivy.uix.screenmanager import Screen

from engine.gfx.py.root.Scene import Scene

class appScreen(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.update(**kwargs)

        if not hasattr(self, 'engine'): raise EnvironmentError
        
        if not hasattr(self, 'autoLaunch'): self.autoLaunch = False
        if not hasattr(self, 'scene'): self.scene = Scene()


        if self.autoLaunch:
            self.load()

    def update(self, **kwargs):
        
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs.get(kwarg))

    def launch(self):
        pass
