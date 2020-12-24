class Tree(object):
    BURNING_AREA = 3

    def __init__(self, intensity):
        self.intensity = intensity
        self.burning = False
        self.burnArea = self.__class__.BURNING_AREA

    def isBurning(self):
        return self.burning

    def setBurning(self):
        self.burning = True

    def tick(self):
        print(self.intensity)
        print("tick")

    def visualize(self):
        print("visualize")


class Shrub(object):
    BURNING_AREA = 2

    def __init__(self, intensity):
        self.intensity = intensity
        self.burning = False
        self.burnArea = self.__class__.BURNING_AREA

    def isBurning(self):
        return self.burning

    def setBurning(self):
        self.burning = True

    def tick(self):
        print("tick")


class Graass(object):
    BURNING_AREA = 3

    def __init__(self, intensity):
        self.intensity = intensity
        self.burning = False
        self.burnArea = self.__class__.BURNING_AREA

    def isBurning(self):
        return self.burning

    def setBurning(self):
        self.burning = True

    def tick(self):
        print("tick")





