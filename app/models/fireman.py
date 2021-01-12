import os
import random


class Firefighter(object):

    def __init__(self, point, name):
        self.point = point
        self.name = name

    def getIcon(self):
        return os.path.join('app', 'resources', 'firefighter.png')

    def setPoint(self, point):
        self.point = point

    def getPoint(self):
        return self.point

    def getName(self):
        return self.name
