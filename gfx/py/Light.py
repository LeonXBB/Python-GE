from gfx.py.Widget import Widget

class Light(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not hasattr(self, "level"): self.level = 0
        if not hasattr(self, "directions"): self.directions = [[None],[None],[None]] 

    def getAdded(self):
        pass

    def getDeleted(self):
        pass

    def move(self, direction):
        super().move(direction)

    def calculateEffect(self):
        pass