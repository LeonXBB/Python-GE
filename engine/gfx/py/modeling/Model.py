from engine.gfx.py.root.Widget import Widget

class Model(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not hasattr(self, "texture"): self.texture = "default"
        if not hasattr(self, "joints"): self.joints = []        
        if not hasattr(self, "poligons"): self.poligons = []