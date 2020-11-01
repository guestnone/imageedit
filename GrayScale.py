from enum import Enum

import cv2
import qimage2ndarray
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog

from GrayScaleDialog import Ui_grayScaleDialog


class SelectedColorChannel(Enum):
    Red = 0,
    Green = 1,
    Blue = 2,
    Unknown = -1


class GrayScaleDialogImpl(QDialog):
    def __init__(self):
        ##
        super(GrayScaleDialogImpl, self).__init__()
        self.ui = Ui_grayScaleDialog()
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
        self.doIt = True
        self.close()

    @pyqtSlot()
    def handleCancel(self):
        self.doIt = False
        self.close()

    def getChannel(self):
        if self.ui.comboBox.currentText() == "Red":
            return SelectedColorChannel.Red
        if self.ui.comboBox.currentText() == "Green":
            return SelectedColorChannel.Green
        if self.ui.comboBox.currentText() == "Blue":
            return SelectedColorChannel.Blue
        return SelectedColorChannel.Unknown

class GrayScale:
    def __init__(self, image):
        self.dialog = GrayScaleDialogImpl()
        self.dialog.setModal(True)
        self.dialog.exec_()
        self.ok = False

        if self.dialog.doIt:
            self.process(image, self.dialog.getChannel())

    def isChanged(self):
        return self.dialog.doIt

    def getAfterQImage(self):
        return qimage2ndarray.array2qimage(self.afterImage)

    def process(self, image, channel):
        input = qimage2ndarray.rgb_view(image, 'little')
        b, g, r = cv2.split(input)

        if channel == SelectedColorChannel.Red:
            self.afterImage = cv2.merge((r, r, r))
        elif channel == SelectedColorChannel.Green:
            self.afterImage = cv2.merge((g, g, g))
        else:
            self.afterImage = cv2.merge((b, b, b))