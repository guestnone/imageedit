from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, pyqtSlot, QAbstractTableModel, QModelIndex, QVariant
from PyQt5.QtGui import *
from ColorSelectDialog import Ui_ColorSelectDialog


class ColorSelectDialog(QDialog):
    def __init__(self, color):
    ##
        super(ColorSelectDialog, self).__init__()
        self.isChange = False
        self.initUI(color)
    ##
    
    def initUI(self, color):
        '''Initializes the GUI'''
        self.ui = Ui_ColorSelectDialog()
        self.ui.setupUi(self)
        self.ui.colorSelectorPushButton.clicked.connect(self.colorButtonOnClick)
        self.ui.redSpinBox.setValue(color[0])
        self.ui.greenSpinBox.setValue(color[1])
        self.ui.blueSpinBox.setValue(color[2])
        
        # Switch the default PyQt5 connectors to our class
        self.ui.buttonBox.accepted.connect(self.handleOK)
        self.ui.buttonBox.rejected.connect(self.handleCancel)
        
        QApplication.processEvents()
        
        self.show()
    
    def getValue(self):
        red = self.ui.redSpinBox.value()
        green = self.ui.greenSpinBox.value()
        blue = self.ui.blueSpinBox.value()
        return qRgb(red, green, blue)
    
    @pyqtSlot()
    def colorButtonOnClick(self):
        color = QColorDialog.getColor()
        if color.isValid():
            cRGB = QColor(color).getRgb()
            self.ui.redSpinBox.setValue(cRGB[0])
            self.ui.greenSpinBox.setValue(cRGB[1])
            self.ui.blueSpinBox.setValue(cRGB[2])
    
    @pyqtSlot()
    def handleOK(self):
        self.isChange = True
        print("Will Change!")
    
    @pyqtSlot()    
    def handleCancel(self):
        self.isChange = False