from time import sleep

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import random

from app.models.plant import *
from app.models.fireman import *
from app.models.point import *
from app.models.fire import *

MAP_SIZE = 10
FIREMAN_COUNT = 3

PLANTS = {
    Tree: 3,
    Grass: 3,
    Shrub: 3
}


class QGameOfLife(QWidget):

    def __init__(self, size=(400, 400)):
        super().__init__()
        self.size = size

        self.generateMap()
        self.initUI()

        self.generatePlants()
        self.generateFireFighter()
        self.generateFire()

        self.show()

    def generateFire(self):
        plants = self.getPlants()

        for s in range(3):
            while True:
                sleep(2)
                try:
                    i = random.randint(0, len(plants) - 1)

                    plant = plants[i]

                    if plant.isBurning():
                        raise

                    fire = Fire(plant, plant.point)
                    fire.setFire()

                    cellItem = self.tableWidget.takeItem(plant.point.x, plant.point.y)

                    cellItem.setBackgroundColor(fire.getColor())

                    self.tableWidget.setItem(plant.point.x, plant.point.y, cellItem)
                except Exception as ex:
                    continue
                break

    def generateFireFighter(self):
        for _ in range(FIREMAN_COUNT):
            while True:
                try:
                    i = random.randint(0, MAP_SIZE - 1)
                    j = random.randint(0, MAP_SIZE - 1)

                    if self.map[i][j].isFree():
                        self.map[i][j].setAccupied()
                        plant = Firefighter(self.map[i][j])
                        self.map[i][j].setElement(plant)

                        item = QTableWidgetItem()
                        item.setIcon(QIcon(plant.getIcon()))
                        self.tableWidget.setItem(i, j, item)
                    else:
                        raise
                except Exception:
                    continue
                break

    def generatePlants(self):
        for k in PLANTS.keys():
            for _ in range(PLANTS[k]):
                while True:
                    try:
                        i = random.randint(0, MAP_SIZE - 1)
                        j = random.randint(0, MAP_SIZE - 1)

                        if self.map[i][j].isFree():
                            self.map[i][j].setAccupied()
                            plant = k(3, self.map[i][j])
                            self.map[i][j].setElement(plant)

                            item = QTableWidgetItem()
                            item.setIcon(QIcon(plant.getIcon()))
                            self.tableWidget.setItem(i, j, item)
                        else:
                            raise
                    except Exception:
                        continue
                    break

    def initUI(self):
        self.setWindowTitle(self.tr("Game of Life"))

        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.item = None
        self.timer = QTimer()
        self.timer.setInterval(10)

        self.createTable()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        self.left = 500
        self.top = 300
        self.width = 600
        self.height = 550

        self.setGeometry(self.left, self.top, self.width, self.height)

    def createTable(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(MAP_SIZE)
        self.tableWidget.setColumnCount(MAP_SIZE)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)

        for i in range(10):
            for j in range(10):
                self.tableWidget.setColumnWidth(i, 50)
                self.tableWidget.setRowHeight(j, 50)

    def generateMap(self):
        self.map = [[Point(i, j) for j in range(MAP_SIZE)] for i in range(MAP_SIZE)]

    def getPlants(self):
        plants = []
        for i in range(len(self.map)):
            for j in range(len(self.map)):
                if self.map[i][j].isPlant():
                    plants.append(self.map[i][j].getElement())

        return plants


if __name__ == '__main__':
    from PySide2.QtWidgets import QApplication
    import sys

    application = QApplication(sys.argv)
    qGameOfLife = QGameOfLife(size=(400, 400))
    sys.exit(application.exec_())
