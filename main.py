from PySide2.QtWidgets import QWidget, QComboBox, QGraphicsScene, QGraphicsView, QVBoxLayout, QFrame, QSizePolicy
from PySide2.QtCore import Qt, QSize, QTimer
from PySide2.QtGui import QImage, QPixmap, QResizeEvent
import random
import numpy as np

from app.models.plant import *


class QGameOfLife(QWidget):

    def __init__(self, size=(400, 400)):
        super(QGameOfLife, self).__init__()
        self.size = size
        self.initUI()
        self.show()

    def initUI(self):
        self.setWindowTitle(self.tr("Game of Life"))
        self.setLayout(QVBoxLayout())
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)


        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
        self.view.setFrameShape(QFrame.NoFrame)
        self.layout().addWidget(self.view)
        #
        # self.item = None
        # self.timer = QTimer()
        # self.timer.setInterval(10)
        # self.view.fitInView(self.item, Qt.KeepAspectRatioByExpanding)


        self.item = None
        self.timer = QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.tick)
        self.select()
        self.view.fitInView(self.item, Qt.KeepAspectRatioByExpanding)

        self.game = Tree(1)
        # self.comboBox.setCurrentText(initialGame)

    def select(self):
        self.timer.stop()
        self.game = Tree(1)
        self.tick()
        self.timer.start()

    def tick(self):
        self.game.tick()
        bitmap = self.game.visualize()

        image = QImage(np.array([1]).data, 128, 128, QImage.Format_Grayscale8)
        self.scene.removeItem(self.item)
        pixmap = QPixmap.fromImage(image)
        self.item = self.scene.addPixmap(pixmap)


    def resizeEvent(self, event: QResizeEvent):
        self.view.fitInView(self.item, Qt.KeepAspectRatioByExpanding)

    def sizeHint(self) -> QSize:
        return QSize(self.size[0], self.size[1])

if __name__ == '__main__':
    from PySide2.QtWidgets import QApplication
    import sys

    application = QApplication(sys.argv)
    qGameOfLife = QGameOfLife(size=(400, 400))
    sys.exit(application.exec_())