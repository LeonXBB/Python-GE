from engine.gfx.py.root.Widget import Widget

class Point(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not hasattr(self, 'occupant'): self.occupant = None
        if not hasattr(self, "widgetColor"): self.widgetColor = [0,0,0,0]
        if not hasattr(self, 'lightLevel'): self.lightLevel = 0

    def calculateColor(self):
        pass