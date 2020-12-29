from .plant import *

FIRE_COLOR_MAP = {
    Tree: "red",
    Grass: "yellow",
    Shrub: "orange"
}


class Fire(object):
    def __init__(self, plant, point):
        self.plant = plant
        self.point = point

    def putOut(self):
        if self.plant.isBurning():
            self.plant.setBurning(False)

    def setFire(self):
        if not self.plant.isBurning():
            self.plant.setBurning(True)

    def getColor(self):
        return FIRE_COLOR_MAP[self.plant.__class__]

    def getPoint(self):
        return self.point


