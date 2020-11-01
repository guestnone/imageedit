from enum import Enum

import cv2
import qimage2ndarray
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox

from ImageOpsDialog import Ui_imageOpsDialog

import numpy as np

class ImageOpsType(Enum):
    Add = 0
    Subtract = 1
    Multiply = 2
    Divide = 3
    Brighten = 4
    Darken = 5
    Unknown = -1


class ImageOpsValueSelect(QDialog):
    def __init__(self):
        ##
        super(ImageOpsValueSelect, self).__init__()
        self.ui = Ui_imageOpsDialog()
        self.doIt = False
        self.initUI()

    ##

    def initUI(self):
        """Initializes the GUI"""
        self.ui.setupUi(self)

        # Switch the default PyQt5 connectors to our class
        self.ui.buttonBox.accepted.connect(self.handleOK)
        self.ui.buttonBox.rejected.connect(self.handleCancel)

        QApplication.processEvents()

        self.show()

    @pyqtSlot()
    def handleOK(self):
        op = self.getOp()
        if op == ImageOpsType.Add or op == ImageOpsType.Subtract or op == ImageOpsType.Multiply or op == ImageOpsType.Divide:
            if not 0 <= self.ui.valueSpinBox.value() <= 255:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Vaule not between 0 and 255!")
                msg.setWindowTitle("Error!")
                msg.exec_()
                return
        self.doIt = True
        self.close()

    @pyqtSlot()
    def handleCancel(self):
        self.doIt = False
        self.close()

    def getOp(self):
        if self.ui.comboBox.currentText() == "Add":
            return ImageOpsType.Add
        if self.ui.comboBox.currentText() == "Subtract":
            return ImageOpsType.Subtract
        if self.ui.comboBox.currentText() == "Multiply":
            return ImageOpsType.Multiply
        if self.ui.comboBox.currentText() == "Divide":
            return ImageOpsType.Divide
        if self.ui.comboBox.currentText() == "Darken":
            return ImageOpsType.Darken
        if self.ui.comboBox.currentText() == "Brighten":
            return ImageOpsType.Brighten
        return ImageOpsType.Unknown


class ImageOps:
    def __init__(self, image):
        self.dialog = ImageOpsValueSelect()
        self.dialog.setModal(True)
        self.dialog.exec_()
        self.ok = False

        if self.dialog.doIt:
            self.ok = self.process(image, self.dialog.getOp(), self.dialog.ui.valueSpinBox.value())


    def isChanged(self):
        return self.dialog.doIt

    def getAfterQImage(self):
        return qimage2ndarray.array2qimage(self.afterImage)

    def process(self, image, type: ImageOpsType, value):
        ## Convert QImage to ndarray and use a helper function to split the image array into 3 channels
        input = qimage2ndarray.rgb_view(image, 'little')
        b, g, r = cv2.split(input)

        if type == ImageOpsType.Add:
            self.newB = np.fmod((b + value), 256)
            self.newG = np.fmod((g + value), 256)
            self.newR = np.fmod((r + value), 256)
        elif type == ImageOpsType.Subtract:
            self.newB = np.where(value <= b, b - value, 0)
            self.newG = np.where(value <= g, g - value, 0)
            self.newR = np.where(value <= r, r - value, 0)
        elif type == ImageOpsType.Multiply:
            self.newB = np.fmod((b * value), 256)
            self.newG = np.fmod((g * value), 256)
            self.newR = np.fmod((r * value), 256)
        elif type == ImageOpsType.Divide:
            self.newB = np.where(value > 0, np.fmod((b / value), 256).astype(int), b)
            self.newG = np.where(value > 0, np.fmod((g / value), 256).astype(int), g)
            self.newR = np.where(value > 0, np.fmod((r / value), 256).astype(int), r)
        elif type == ImageOpsType.Darken:
            # Use of the exponential gives us very large values, so we do a modulo to get value in our range
            self.newB = np.fmod(value * np.exp2(b.astype(int)), 256)
            self.newG = np.fmod(value * np.exp2(g.astype(int)), 256)
            self.newR = np.fmod(value * np.exp2(r.astype(int)), 256)

            self.newB[self.newB > 255] = 255
            self.newB[self.newB < 0] = 0
            self.newG[self.newG > 255] = 255
            self.newG[self.newG < 0] = 0
            self.newR[self.newR > 255] = 255
            self.newR[self.newR < 0] = 0

        elif type == ImageOpsType.Brighten:
            self.newB = (value * np.log10(b + 1)).astype(int)
            self.newG = (value * np.log10(g + 1)).astype(int)
            self.newR = (value * np.log10(r + 1)).astype(int)

            self.newB[self.newB > 255] = 255
            self.newB[self.newB < 0] = 0
            self.newG[self.newG > 255] = 255
            self.newG[self.newG < 0] = 0
            self.newR[self.newR > 255] = 255
            self.newR[self.newR < 0] = 0

        else: # unknown operation
            return False

        img_out = cv2.merge((self.newR, self.newG, self.newB))
        self.afterImage = img_out
        return True

