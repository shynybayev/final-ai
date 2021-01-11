import os

class Plant(object):

    def __init__(self, point):
        self.point =  point

    def getPoint(self):
        return self.point

    def getPointAsInt(self):
        return (self.point.x + 1) * (self.point.y + 1)

class Tree(Plant):
    BURNING_AREA = 3

    def __init__(self, intensity, point):
        super().__init__(point)
        self.intensity = intensity
        self.burning = False
        self.burnArea = self.__class__.BURNING_AREA

    def isBurning(self):
        return self.burning

    def setBurning(self, val):
        self.burning = val

    def tick(self):
        print(self.intensity)
        print("tick")

    def visualize(self):
        print("visualize")

    def text(self):
        return f"Tree at point {self.point.x} and {self.point.y}"

    def getIcon(self):
        return os.path.join('app', 'resources', 'tree.png')




class Shrub(Plant):
    BURNING_AREA = 2

    def __init__(self, intensity, point):
        super().__init__(point)
        self.intensity = intensity
        self.burning = False
        self.burnArea = self.__class__.BURNING_AREA

    def isBurning(self):
        return self.burning

    def setBurning(self, val):
        self.burning = val

    def tick(self):
        print("tick")

    def getIcon(self):
        return os.path.join('app', 'resources', 'shrub.jpg')


class Grass(Plant):
    BURNING_AREA = 3

    def __init__(self, intensity, point):
        super().__init__(point)
        self.intensity = intensity
        self.burning = False
        self.burnArea = self.__class__.BURNING_AREA

    def isBurning(self):
        return self.burning

    def setBurning(self, val):
        self.burning = val

    def tick(self):
        print("tick")

    def getIcon(self):
        return os.path.join('app', 'resources', 'grass.png')
