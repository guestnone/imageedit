from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, pyqtSlot, QAbstractTableModel, QModelIndex, QVariant
from PyQt5.QtGui import *


class HistogramWidget(QWidget):    
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)        
        self.canvas = FigureCanvas(Figure())
       
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        
        self.canvas.sumbu1 = self.canvas.figure.add_subplot(111)
        self.canvas.figure.set_facecolor("xkcd:wheat")
        self.setLayout(vertical_layout)