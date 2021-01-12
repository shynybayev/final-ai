from concurrent.futures.thread import ThreadPoolExecutor
from time import sleep
import aiohttp
from PySide2.QtWidgets import *
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PySide2.QtGui import *
import random
import asyncio
import copy
from app.models.plant import *
from app.models.fireman import *
from app.models.point import *
from app.models.fire import *
from app.models.models import *

MAP_SIZE = 5
FIREMAN_COUNT = 1

PLANTS = {
    Tree: 2,
    Grass: 2,
    Shrub: 2
}


class Environment(QWidget):

    def __init__(self, size=(400, 400)):
        super().__init__()

        self.plants = []
        self.map = []
        self.firefighters = []
        self.initialFireFightersPoint = []
        self.initialPlantPoint = []
        self.initialFirePoint = []
        self.fire = []

        self.d = {}
        self.f = {}
        self.i = 0
        self.c = True

        self.longest = 0
        self.shortest = 0

        self.size = size
        self.generateMap()
        self.initUI()
        self.generatePlants()
        self.generateFireFighter()
        self.generateFire()
        self.show()
        self.run()

    def generateFire(self):
        if len(self.initialFirePoint) > 0:
            for i in range(len(self.initialFirePoint)):
                fire = self.initialFirePoint[i]
                self.fire.append(fire)
                fire.setFire()

                cellItem = self.tableWidget.takeItem(fire.point.x, fire.point.y)
                cellItem.setBackgroundColor(fire.getColor())
                self.tableWidget.setItem(fire.point.x, fire.point.y, cellItem)
            return

        for s in range(1):
            while True:
                try:
                    i = random.randint(0, len(self.plants) - 1)
                    plant = self.plants[i]

                    if plant.isBurning():
                        raise

                    fire = Fire(plant, plant.point)
                    fire.setFire()

                    self.fire.append(fire)
                    self.initialFirePoint.append(fire)

                    cellItem = self.tableWidget.takeItem(plant.point.x, plant.point.y)
                    cellItem.setBackgroundColor(fire.getColor())
                    self.tableWidget.setItem(plant.point.x, plant.point.y, cellItem)
                except Exception as ex:
                    continue
                break

    def generateFireFighter(self):
        if len(self.initialFireFightersPoint) > 0:

            for i in range(len(self.initialFireFightersPoint)):
                point = self.initialFireFightersPoint[i]
                self.map[point.x][point.y].setAccupied()
                firefighter = Firefighter(self.map[point.x][point.y])
                self.map[point.x][point.y].setElement(firefighter)

                self.firefighters.append(firefighter)

                item = QTableWidgetItem()
                item.setIcon(QIcon(firefighter.getIcon()))
                self.tableWidget.setItem(point.x, point.y, item)
            return
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
                        self.initialFireFightersPoint.append(copy.deepcopy(self.map[i][j]))

                        item = QTableWidgetItem()
                        item.setIcon(QIcon(firefighter.getIcon()))
                        self.tableWidget.setItem(i, j, item)
                    else:
                        raise
                except Exception:
                    continue
                break

    def generatePlants(self):
        if len(self.initialPlantPoint) > 0:
            for i in range(len(self.initialPlantPoint)):
                for k in self.initialPlantPoint[i].keys():
                    point = self.initialPlantPoint[i][k]


                    self.map[point.x][point.y].setAccupied()
                    self.plants.append(k)
                    self.map[point.x][point.y].setElement(k)

                    item = QTableWidgetItem()
                    item.setIcon(QIcon(k.getIcon()))
                    self.tableWidget.setItem(point.x, point.y, item)

            return

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

                            self.plants.append(plant)
                            self.initialPlantPoint.append({plant: copy.deepcopy(self.map[i][j])})

                            item = QTableWidgetItem()
                            item.setIcon(QIcon(plant.getIcon()))
                            self.tableWidget.setItem(i, j, item)
                        else:
                            raise
                    except Exception:
                        continue
                    break

    def initUI(self):
        self.setWindowTitle(self.tr("FireFighters"))

        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

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

    def runInThread(self, loop):
        asyncio.set_event_loop(loop)
        # asyncio.sleep(2)
        loop.run_until_complete(self.tick2())
        # loop.close(self)

    def run(self):
        import threading

        loop = asyncio.get_event_loop()
        th = threading.Thread(target=self.runInThread, args=(loop,))
        th.start()

        # task1 = asyncio.create_task(self.move_first_fireman())
        # task2 = asyncio.create_task(self.move_first_fireman_1())
        # await asyncio.gather(task1, task2)
        # import threading
        # threads = []
        # loop = asyncio.get_event_loop()
        # loop2 = asyncio.get_event_loop()
        # for i in range(5):
        # loop2 = asyncio.get_event_loop()
        # th = threading.Thread(target=self.runInThread,args=(loop,))
        # th.start()
        # th2 = threading.Thread(target=self.runInThread2,args=(loop2,))
        # th2.start()

    def showUi(self):

        import threading

        thread = threading.Thread(target=self.show)
        thread.start()


    def reset(self):
        self.firefighters = []
        self.fire = []
        self.plants = []

        self.d = {}
        self.i = 0

        self.generateMap()
        self.generatePlants()
        self.generateFireFighter()
        self.generateFire()


        return self.initialFireFightersPoint[0]

    def step(self, action):
        # Current state of the agent
        fireman = self.firefighters[0]
        point = copy.deepcopy(fireman.getPoint())


        if action == 0:    # налево
            if point.y > 0:
                self.map[point.x][point.y - 1].setAccupied()
                self.map[point.x][point.y - 1].setElement(fireman)
                self.map[point.x][point.y].setFree()

                self.tableWidget.setItem(point.x, point.y, QTableWidgetItem())

                point.y = point.y - 1

                item = self.tableWidget.takeItem(point.x, point.y)
                if item is None:
                    item = QTableWidgetItem()
                item.setBackgroundColor("green")
                self.tableWidget.setItem(point.x, point.y, item)

        elif action == 1:  # вверх
            if point.x > 0:
                self.map[point.x - 1][point.y].setAccupied()
                self.map[point.x - 1][point.y].setElement(fireman)
                self.map[point.x][point.y].setFree()

                self.tableWidget.setItem(point.x, point.y, QTableWidgetItem())

                point.x = point.x - 1
                item = self.tableWidget.takeItem(point.x, point.y)
                if item is None:
                    item = QTableWidgetItem()
                item.setBackgroundColor("green")
                self.tableWidget.setItem(point.x, point.y, item)

        elif action == 2:  # направо
            if point.y < MAP_SIZE - 1:
                self.map[point.x][point.y + 1].setAccupied()
                self.map[point.x][point.y + 1].setElement(fireman)
                self.map[point.x][point.y].setFree()

                self.tableWidget.setItem(point.x, point.y, QTableWidgetItem())

                point.y = point.y + 1
                item = self.tableWidget.takeItem(point.x, point.y)
                if item is None:
                    item = QTableWidgetItem()
                item.setBackgroundColor("green")
                self.tableWidget.setItem(point.x, point.y, item)

        elif action == 3:  # вниз
            if point.x < MAP_SIZE - 1:
                self.map[point.x + 1][point.y].setAccupied()
                self.map[point.x + 1][point.y].setElement(fireman)
                self.map[point.x][point.y].setFree()

                self.tableWidget.setItem(point.x, point.y, QTableWidgetItem())


                point.x = point.x + 1
                item = self.tableWidget.takeItem(point.x, point.y)
                if item is None:
                    item = QTableWidgetItem()
                item.setBackgroundColor("green")
                self.tableWidget.setItem(point.x, point.y, item)

        cellItem = self.tableWidget.takeItem(point.x, point.y)

        if cellItem is None:
            cellItem = QTableWidgetItem()

        if not self.map[point.x][point.y].isPlant():
           cellItem.setIcon(QIcon(fireman.getIcon()))

        self.tableWidget.setItem(point.x, point.y, cellItem)

        fpoint = fireman.getPoint()
        fpoint.x = point.x
        fpoint.y = point.y
        fireman.setPoint(fpoint)
        print("after action point:" + str(point))


        self.d[self.i] = point

        next_state = self.d[self.i]

        firePoint = self.fire[0].getPoint()


        self.i += 1

        # print(list(map(lambda x: x.getPoint(), self.plants)))
        if next_state.x == firePoint.x and next_state.y == firePoint.y:
            reward = 1
            done = True
            next_state = 'goal'

            if self.c == True:
                for j in range(len(self.d)):
                    self.f[j] = self.d[j]
                self.c = False
                self.longest = len(self.d)
                self.shortest = len(self.d)

            if len(self.d) < len(self.f):
                self.shortest = len(self.d)
                self.f = {}
                for j in range(len(self.d)):
                    self.f[j] = self.d[j]

            if len(self.d) > self.longest:
                self.longest = len(self.d)

        elif len(list(filter(lambda x: x.getPoint().x == next_state.x and x.getPoint().y == next_state.y, self.plants))) > 0:
            reward = -1
            done = True
            next_state = 'obstacle'

            # Очистка значении в dictionary и его коунтера i
            self.d = {}
            self.i = 0

        else:
            # next_state = (next_state.x + 1) * (next_state.y + 1)
            reward = 0
            done = False

        return next_state, reward, done

    async def iterate_over_firemans(self):
        futures = []
        for i in range(len(self.firefighters)):
            futures.append(self.move_fireman(self.firefighters[i]))

        await asyncio.gather(*futures)

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

    def final(self):

        self.initial_point = self.initialFireFightersPoint[0]
        a = {}
        for j in range(len(self.f)):
            # print(self.f[j])

            item = QTableWidgetItem()
            item.setBackgroundColor("black")

            self.tableWidget.setItem(self.f[j].x, self.f[j].y, item)

            a[j] = self.f[j]

        return a

    from _datetime import datetime

    async def tick2(self):
        print(self.datetime.now())
        print("ticker")
        goal = False
        steps = []
        all_costs = []
        for episode in range(100):
            print("start: " + str(episode))

            observation = self.reset()
            print(str(observation) + ": " + str(observation.x * MAP_SIZE + observation.y))
            observation = observation.x * MAP_SIZE + observation.y

            i = 0
            cost = 0
            while True:

                sleep(0.5)
                print(observation)
                action = RL.choose_action(observation)

                a = {
                    0: "left",
                    1: "up",
                    2: "right",
                    3: "down",
                }

                print(a[action])
                observation_, reward, done = self.step(action)

                if type(observation_) != str:
                    if type(observation_) == Point:
                        observation_ = observation_.x * MAP_SIZE + observation_.y


                cost += RL.learn(observation, action, reward, observation_)
                observation = observation_
                if observation_ == "goal":
                    goal = True

                i += 1

                if done:
                    steps += [i]
                    all_costs += [cost]
                    break
            # if goal:
            #     break

        a = self.final()
        RL.print_q_table(a)
        RL.plot_results(steps, all_costs)

RL = QLearningTable(actions=list(range(4)))

if __name__ == '__main__':
    from PySide2.QtWidgets import QApplication
    import sys

    application = QApplication(sys.argv)
    env = Environment()

    sys.exit(application.exec_())
