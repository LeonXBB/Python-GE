from gfx.py.Widget import Widget


from gfx.py.Widget import Widget
from gfx.py.Camera import Camera

class Scene:

    def __init__(self, engine, **kwargs):

        self.engine = engine

        if not hasattr(self, "widgets"): self.widgets = []
        if not hasattr(self, "content"): self.content = [[],[],[]]
        if not hasattr(self, "lights"): self.lights = []
        if not hasattr(self, "instructions"): self.instructions = []
        if not hasattr(self, "camera"): self.camera = Camera(self)

    def add_widget(self, widget, index, canvas):
        return super().add_widget(widget, index=index, canvas=canvas)

    def remove_widget(self, widget):
        return super().remove_widget(widget)

    def calculateInstructions(self):
        pass

    def executeInstructions(self):
        pass

    def calculateContent(self):
        pass