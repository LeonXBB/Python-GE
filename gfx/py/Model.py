from gfx.py.Widget import Widget

class Model(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not hasattr(self, "texture"): self.texture = "default"


