# importing libraries
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # setting title and window properties
        self.setWindowTitle("On Screen detection")
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NoSystemBackground)
        # setting geometry
        self.setGeometry(100, 100, 600, 400)

        # calling method
        self.UiComponents()
        # showing all the widgets
        self.show()

    # def paintEvent(self, QPaintEvent):
    #     bbox = [40, 40, 400, 200]
    #     painter = QPainter()
    #     painter.begin(self)
    #     self.drawbbox(bbox,painter)
    #     painter.end()
    #
    # def drawbbox(self, bbox, painter):
    #     x, y, x_len, y_len = bbox
    #     painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
    #     painter.drawRect(x, y, x_len, y_len)

    def paintEvent(self, event):
       qp = QPainter()
       qp.begin(self)

       qp.setPen(QtGui.QColor(200, 0, 0))
       qp.drawText(20, 20, "Text at fixed coordinates")
       qp.drawText(event.rect(), Qt.AlignCenter, "Text centerd in the drawing area")
       qp.setPen(QtGui.QPen(Qt.darkGreen, 4))
       qp.drawEllipse(QPoint(50, 60), 30, 30)
       qp.setPen(QtGui.QPen(Qt.blue, 2, join=Qt.MiterJoin))
       qp.drawRect(20, 60, 50, 80)

       qp.end()

    def UiComponents(self):
        # # creating label
        # label = QLabel("Label", self)
        #
        # # setting geometry to label
        # label.setGeometry(100, 100, 120, 40)
        #
        # # adding border to label
        # label.setStyleSheet("border : 2px solid black")
        # opening window in maximized size
        bbox = [40, 40, 400, 200]

        self.paintEvent(QPaintEvent)
        self.showMaximized()


if __name__ == '__main__':
    App = QApplication(sys.argv)

    # create the instance of our Window
    window = Window()

    # start the app
    sys.exit(App.exec())
