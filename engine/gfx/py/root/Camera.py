from engine.gfx.py.root.Widget import Widget

class Camera(Widget):

    def __init__(self, scene, **kwargs):
        super().__init__(**kwargs)

        if not hasattr(self, "currentAngle"): self.currentAngle = 90
        if not hasattr(self, 'currentZoom'): self.currentZoom = 1
        if not hasattr(self, 'objectCentred'): self.objectCentred = None
        if not hasattr(self, 'objectFollowed'): self.objectFollowed = None
        if not hasattr(self, 'frozen'): self.frozen = False

    def move(self, direction):
        super().move(direction)

    def changeZoom(self, newLevel):
        pass

    def freeze(self):
        pass

    def center(self, object=None, direction=None, distance=None):
        pass

    def follow(self, object=None, direction=None, distance=None):
        pass

    def unCenter(self):
        pass

    def unFollow(self):
        pass

    def unFreeze(self):
        pass

    def getCanvas(self):
        pass