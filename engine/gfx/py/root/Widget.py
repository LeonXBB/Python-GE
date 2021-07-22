from kivy.uix.widget import Widget as kivyWidget

class Widget(kivyWidget):

    def __init__(self, **kwargs):

        super().__init__() #TODO find a way to add kwargs to kivyWidget. Currently it's not working due to kwargs having parameters not implimented in kivyWidget. (see https://stackoverflow.com/questions/57672872/typeerror-object-init-takes-exactly-one-argument-the-instance-to-initial#comment101792794_57672872)

        self.update(**kwargs)

        if not hasattr(self, 'engine'): raise EnvironmentError

        if not hasattr(self, "widgetSize"): self.widgetSize = [self.engine.engineSettings.windowWidth, self.engine.engineSettings.windowHeight, 1]
        if not hasattr(self, "widgetPos"): self.widgetPos = [0, 0, 0]
        if not hasattr(self, "widgetPadding"): self.widgetPadding = [None, None, None, None]
        if not hasattr(self, "widgetSpacing"): self.widgetSpacing = [None, None]
        
        if not hasattr(self, 'associatedSound'): self.associatedSound = None

        if not hasattr(self, "physicalProperties"): self.physicalProperties = None # TODO Change

        if not hasattr(self, "switchCoordinates"): self.switchCoordinates = self.engine.GUIThread.switchCoordinates

    def update(self, **kwargs):
        
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs.get(kwarg))

    def move(self, direction):
        pass

    def addAssociatedSound(self, sound):
        pass

    def deleteAssociatedSound(self, sound):
        pass