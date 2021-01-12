from time import sleep

from PySide2.QtWidgets import *

from PySide2.QtGui import *
import threading
import asyncio
import copy

from app.models.plant import *
from app.models.fireman import *
from app.models.point import *
from app.models.fire import *
from app.models.models import *

from app.services.services import *

MAP_SIZE = 5
FIREMAN_COUNT = 2

FIRE_COUNT = 2

FIREMAN_COLOR = {
    1: "red",
    2: "yellow",
    3: "green"
}

PLANTS = {
    Tree: 2,
    Grass: 2,
    Shrub: 2
}


class Environment(QWidget):

    def __init__(self, size=(400, 400)):
        super().__init__()

        self._lock = threading.Lock()


        # initialize base elements
        self.plants = []
        self.map = []
        self.firefighters = []
        self.initialFireFightersPoint = {}
        self.initialPlantPoint = []
        self.initialFirePoint = []
        self.fire = []

        # для хранения пути
        self.d = {}

        # для хранения конечной пути
        self.f = {}

        # кол-во ходов
        self.i = {}

        # нужен при первом запуске
        self.c = {}

        self.size = size
        self.generateMap()
        self.initUI()
        self.generatePlants()
        self.generateFireFighter()
        self.generateFire()
        self.learningTables = {}
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

        for s in range(FIRE_COUNT):
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

    def generateFireFighter(self, fireman=None):
        if fireman is not None:
            point = self.initialFireFightersPoint[fireman.getName()]
            self.map[point.x][point.y].setAccupied()
            firefighter = Firefighter(self.map[point.x][point.y], fireman.getName())
            self.map[point.x][point.y].setElement(firefighter)

            self.firefighters.append(firefighter)

            item = QTableWidgetItem()
            item.setIcon(QIcon(firefighter.getIcon()))
            self.tableWidget.setItem(point.x, point.y, item)

            return firefighter

        for firemanOrder in range(FIREMAN_COUNT):
            while True:
                try:
                    i = random.randint(0, MAP_SIZE - 1)
                    j = random.randint(0, MAP_SIZE - 1)

                    if self.map[i][j].isFree():
                        self.map[i][j].setAccupied()
                        firefighter = Firefighter(self.map[i][j], firemanOrder)
                        self.map[i][j].setElement(firefighter)

                        self.firefighters.append(firefighter)
                        self.initialFireFightersPoint[firemanOrder] = copy.deepcopy(self.map[i][j])

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

                            # store plants
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
        tasks = []

        for i in range(len(self.firefighters)):
            fireman = self.firefighters[i]

            learner = QLearningTable(actions=list(range(4)))
            self.learningTables[fireman.getName()] = learner

            task = loop.create_task(self.tick2(fireman))
            tasks.append(task)
            # loop.run_until_complete(self.tick2(fireman))

        print(len(tasks))
        # await asyncio.wait(*tasks)
        loop.run_until_complete(asyncio.wait(tasks))


    def run(self):

        # loop = asyncio.get_event_loop()
        # t = threading.Thread(target=self.runInThread, args=(loop,))
        # t.start()
        # t.join()

        # future = asyncio.run_coroutine_threadsafe(self.runInThread(loop), loop)
        # result = future.result()
        # thread = threading.Thread(target=future.result)
        #
        # thread.start()
        # thread.join()

        for i in range(len(self.firefighters)):

            fireman = self.firefighters[i]
            learner = QLearningTable(actions=list(range(4)))
            self.learningTables[fireman.getName()] = learner
            sleep(1)

            thread = threading.Thread(target=self.tick2, args=(fireman,))
            # threads.append(thread)
            thread.start()
            # thread.join()

        # for i in range(len(threads)):
        #     threads[i].start()
        #     threads[i].join()

    def showUi(self):

        import threading

        thread = threading.Thread(target=self.show)
        thread.start()

    def tick(self):

        # self.timer.stop()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        while True:
            # loop = asyncio.get_event_loop()
            sleep(2)
            print("tick")
            loop.run_until_complete(self.iterate_over_firemans())
        #
        # self.timer.start()

    def reset(self, fireman):


            # try:
        with self._lock:
            for i in range(len(self.firefighters)):
                    # print(i)
                    # print(self.firefighters[i])
                    # print(fireman)
                    # print(i)
                if self.firefighters[i].getName() == fireman.getName():
                    # del self.firefighters[i]
                    self.firefighters.pop(i)
                    break
            print("fireman number: " + str(fireman.getName()))

            self.fire = []
            self.plants = []

            self.d[fireman.getName()] = {}
            self.i[fireman.getName()] = 0

            self.generateMap()
            self.generatePlants()
            firemanNew = self.generateFireFighter(fireman)
            self.generateFire()

            return firemanNew, self.initialFireFightersPoint[fireman.getName()]
            # except:
            #     pass
            #     # return self.reset(fireman)


    def step(self, action, fireman):
        point = copy.deepcopy(fireman.getPoint())


        if action == 0:    # left
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

        elif action == 1:  # up
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

        elif action == 2:  # right
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

        elif action == 3:  # down
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

        if fireman.getName() not in list(self.d.keys()):
            self.d[fireman.getName()] = {}

        if fireman.getName() not in list(self.i.keys()):
            self.i[fireman.getName()] = 0

        if fireman.getName() not in list(self.f.keys()):
            self.f[fireman.getName()] = {}

        if fireman.getName() not in list(self.c.keys()):
            self.c[fireman.getName()] = True

        self.d[fireman.getName()][self.i[fireman.getName()]] = point

        next_state = self.d[fireman.getName()][self.i[fireman.getName()]]

        firePoint = self.fire[0].getPoint()

        self.i[fireman.getName()] += 1

        # если нашли огонь
        if next_state.x == firePoint.x and next_state.y == firePoint.y:
            reward = 1
            done = True
            next_state = 'goal'

            # сохраняем путь до огня первый раз
            if self.c[fireman.getName()] == True:
                for j in range(len(self.d[fireman.getName()])):
                    self.f[fireman.getName()][j] = self.d[fireman.getName()][j]
                self.c[fireman.getName()] = False

            # если это более короткий путь до огня
            if len(self.d[fireman.getName()]) < len(self.f[fireman.getName()]):
                self.f[fireman.getName()] = {}
                for j in range(len(self.d[fireman.getName()])):
                    self.f[fireman.getName()][j] = self.d[fireman.getName()][j]

        # нашли преграду
        elif len(list(filter(lambda x: x.getPoint().x == next_state.x and x.getPoint().y == next_state.y, self.plants))) > 0:
            reward = -1
            done = True
            next_state = 'obstacle'

            self.d[fireman.getName()] = {}
            self.i[fireman.getName()] = 0

        else:
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

        if i == 0:  # left
            if point.y > 0 and self.map[point.x][point.y - 1].isFree():
                self.map[point.x][point.y - 1].setAccupied()
                self.map[point.x][point.y].setFree()
                cellItem = self.tableWidget.takeItem(point.x, point.y)
                cellItem.setIcon(QIcon())
                point.y = point.y - 1
        elif i == 1:  # up
            if point.x > 0 and self.map[point.x - 1][point.y].isFree():
                self.map[point.x - 1][point.y].setAccupied()
                self.map[point.x][point.y].setFree()
                cellItem = self.tableWidget.takeItem(point.x, point.y)
                cellItem.setIcon(QIcon())
                point.x = point.x - 1
        elif i == 2:  # right
            if point.y < MAP_SIZE - 1 and self.map[point.x][point.y + 1].isFree():
                self.map[point.x][point.y + 1].setAccupied()
                self.map[point.x][point.y].setFree()
                cellItem = self.tableWidget.takeItem(point.x, point.y)
                cellItem.setIcon(QIcon())
                point.y = point.y + 1
        elif i == 3:  # down
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

    def final(self, fireman):
        self.initial_point = self.initialFireFightersPoint[fireman.getName()]
        a = {}

        for j in range(len(self.f[fireman.getName()])):

            item = QTableWidgetItem()
            item.setBackgroundColor(FIREMAN_COLOR[fireman.getName()])

            self.tableWidget.setItem(self.f[fireman.getName()][j].x, self.f[fireman.getName()][j].y, item)


            a[j] = self.f[fireman.getName()][j]

        return a

    def tick2(self, fireman):
        print("ticker " + str(fireman.getName()))
        learner = self.learningTables[fireman.getName()]

        steps = []
        all_costs = []
        for episode in range(100):
            print("start: " + str(episode))

            fireman, observation = self.reset(fireman)
            print(str(observation) + ": " + str(observation.x * MAP_SIZE + observation.y))
            observation = observation.x * MAP_SIZE + observation.y

            i = 0
            cost = 0
            while True:

                sleep(0.5)
                print(str(observation))
                action = learner.choose_action(observation)

                a = {
                    0: "left",
                    1: "up",
                    2: "right",
                    3: "down",
                }

                print(a[action])
                observation_, reward, done = self.step(action, fireman)

                if type(observation_) != str:
                    if type(observation_) == Point:
                        observation_ = observation_.x * MAP_SIZE + observation_.y

                cost += learner.learn(observation, action, reward, observation_)
                observation = observation_

                i += 1

                if done:
                    steps += [i]
                    all_costs += [cost]
                    break

        a = self.final(fireman)
        learner.print_q_table(a)
        learner.plot_results(steps, all_costs)


if __name__ == '__main__':
    from PySide2.QtWidgets import QApplication
    import sys

    application = QApplication(sys.argv)
    env = Environment()

    sys.exit(application.exec_())
