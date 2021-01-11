from .plant import *
from .fire import *
from .fireman import *


class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.accupied = False
        self.element = None

    def __getitem__(self, item):
        return self

    def isFree(self):
        return not self.accupied

    def setAccupied(self):
        self.accupied = True

    def setFree(self):
        self.accupied = False

    def setElement(self, el):
        self.element = el

    def getElement(self):
        return self.element

    def isPlant(self):
        return self.element.__class__ in [Tree, Grass, Shrub]

    def isFire(self):
        return self.element.__class__ in [Fire]

    def isFireFighter(self):
        return self.element.__class__ in [Firefighter]

    def __str__(self):
        return f"({self.x}, {self.y})"
