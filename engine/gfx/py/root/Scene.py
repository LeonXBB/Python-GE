from engine.gfx.py.root.Camera import Camera

class Scene:

    def __init__(self, engine, **kwargs):

        self.engine = engine

        if not hasattr(self, "models"): self.models = []
        if not hasattr(self, "content"): self.content = [[],[],[]]
        if not hasattr(self, "lights"): self.lights = []
        if not hasattr(self, "instructions"): self.instructions = []
        if not hasattr(self, "camera"): self.camera = Camera(self)

    def addModel(self, widget, index, canvas):
        return super().add_widget(widget, index=index, canvas=canvas)

    def removeModel(self, widget):
        return super().remove_widget(widget)

    def calculateInstructions(self):
        pass

    def executeInstructions(self):
        pass

    def calculateContent(self):
        pass