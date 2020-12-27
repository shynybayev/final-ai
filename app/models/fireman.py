import os

class Firefighter(object):

    def __init__(self, point):
        self.point = point

    def getIcon(self):
        return os.path.join('app', 'resources', 'firefighter.png')
