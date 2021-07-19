from kivy.uix.widget import Widget as kivyWidget

class Widget(kivyWidget):

    def __init__(self, **kwargs):

        super().__init__() #TODO find a way to add kwargs to kivyWidget. Currently it's not working due to kwargs having parameters not implimented in kivyWidget. (see https://stackoverflow.com/questions/57672872/typeerror-object-init-takes-exactly-one-argument-the-instance-to-initial#comment101792794_57672872)

        self.update(**kwargs)

        self.switchCoordinates = self.engine.GUIThread.switchCoordinates

    def update(self, **kwargs):
        
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs.get(kwarg))