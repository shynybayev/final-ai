import os
import random


class Firefighter(object):

    def __init__(self, point):
        self.point = point

    def getIcon(self):
        return os.path.join('app', 'resources', 'firefighter.png')

    def setPoint(self, point):
        self.point = point

    def getPoint(self):
        return self.point
