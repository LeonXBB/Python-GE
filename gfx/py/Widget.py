from kivy.uix.widget import Widget as kivyWidget

class Widget(kivyWidget):

    def __init__(self, **kwargs):

        super().__init__()

        self.update(**kwargs)

        self.switchCoordinates = self.engine.GUIThread.switchCoordinates

    def update(self, **kwargs):
        
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs.get(kwarg))