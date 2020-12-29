import asyncio

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from app.models.fire import *
from app.models.fireman import *
from app.models.point import *
from app.services.agent import *

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
        self.d = {}
        self.i = 0
        self.action_space = ['up', 'down', 'left', 'right']
        self.size = size
        self.generateMap()
        self.initUI()
        self.generatePlants()
        self.generateFireFighter()
        self.generateFire()
        self.show()
        # self.startQLearningRun()
        self.run()

    def generateFire(self):
        plants = self.getPlants()

        for s in range(3):
            while True:
                # sleep(2)
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
        self.firefighters = []

        for _ in range(FIREMAN_COUNT):
            while True:
                try:
                    i = random.randint(0, MAP_SIZE - 1)
                    j = random.randint(0, MAP_SIZE - 1)

                    if self.map[i][j].isFree():
                        self.map[i][j].setAccupied()
                        firefighter = Firefighter(self.map[i][j])
                        self.map[i][j].setElement(firefighter)
                        self.firefighters.append(firefighter)

                        item = QTableWidgetItem()
                        item.setIcon(QIcon(firefighter.getIcon()))
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

    def render(self):
        self.tableWidget.update()
    def final(self, fireman):
        self.tableWidget.deleteLater(fireman)
    def reset(self, fireman):
        self.tableWidget.update()
        self.tableWidget.deleteLater(fireman)

    def generateMap(self):
        self.map = [[Point(i, j) for j in range(MAP_SIZE)] for i in range(MAP_SIZE)]

    def getPlants(self):
        self.plants = []
        for i in range(len(self.map)):
            for j in range(len(self.map)):
                if self.map[i][j].isPlant():
                    self.plants.append(self.map[i][j].getElement())

        return self.plants

    def run(self):
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.tick)
        self.timer.start()


    def tick(self):
        self.timer.stop()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.iterate_over_firemans())
        self.timer.start()
    # def startQLearningRun(self):


    async def iterate_over_firemans(self):
        futures = []
        for i in range(len(self.firefighters)):
            futures.append(self.move_fireman(self.firefighters[i]))
            # futures.append(self.move_fireman_qlearning(self.firefighters[i]))
        asyncio.gather(*futures)

    async def move_fireman_qlearning(self, fireman):
        qLearnTable = QLearningTable(actions=list(range(len(self.action_space))))
        # qLearnTable.update(100, list[fireman.getPoint()], fireman)
        qLearnTable.update(100, fireman)
        action = qLearnTable.choose_action(fireman.getPoint())
        self.move_fireman(fireman)


    async def move_fireman(self, fireman):
        point = fireman.getPoint()
        i = random.randint(0, 3)
        if i == 0:  # налево
            if point.y > 0 and self.map[point.x][point.y - 1].isFree():
                self.map[point.x][point.y - 1].setAccupied()
                self.map[point.x][point.y].setFree()
                cellItem = self.tableWidget.takeItem(point.x, point.y)
                cellItem.setIcon(QIcon())
                point.y = point.y - 1
        elif i == 1:  # вверх
            if point.x > 0 and self.map[point.x - 1][point.y].isFree():
                self.map[point.x - 1][point.y].setAccupied()
                self.map[point.x][point.y].setFree()
                cellItem = self.tableWidget.takeItem(point.x, point.y)
                cellItem.setIcon(QIcon())
                point.x = point.x - 1
        elif i == 2:  # направо
            if point.y < MAP_SIZE - 1 and self.map[point.x][point.y + 1].isFree():
                self.map[point.x][point.y + 1].setAccupied()
                self.map[point.x][point.y].setFree()
                cellItem = self.tableWidget.takeItem(point.x, point.y)
                cellItem.setIcon(QIcon())
                point.y = point.y + 1
        elif i == 3:  # вниз
            if point.x < MAP_SIZE - 1 and self.map[point.x + 1][point.y].isFree():
                self.map[point.x + 1][point.y].setAccupied()
                self.map[point.x][point.y].setFree()
                cellItem = self.tableWidget.takeItem(point.x, point.y)
                cellItem.setIcon(QIcon())
                point.x = point.x + 1

        cellItem = self.tableWidget.takeItem(point.x, point.y)
        if cellItem is None:
            cellItem = QTableWidgetItem()
            cellItem.setIcon(QIcon(fireman.getIcon()))

        self.tableWidget.setItem(point.x, point.y, cellItem)

if __name__ == '__main__':
    from PySide2.QtWidgets import QApplication
    import sys

    application = QApplication(sys.argv)
    qGameOfLife = QGameOfLife(size=(400, 400))
    sys.exit(application.exec_())
