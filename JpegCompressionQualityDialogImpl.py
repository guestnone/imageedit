from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QDialog, QApplication

from JpegCompressionQualityDialog import Ui_JpegCompressionQualityDialog


class JpegCompressionQualityDialog(QDialog):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_JpegCompressionQualityDialog()
        self.save = False
        self.initUI()

    def initUI(self):
        '''Initializes the GUI'''
        self.ui.setupUi(self)

        # Switch the default PyQt5 connectors to our class
        self.ui.buttonBox.accepted.connect(self.handleOK)
        self.ui.buttonBox.rejected.connect(self.handleCancel)

        QApplication.processEvents()

    def getValue(self):
        return self.ui.horizontalSlider.value()

    def getSave(self):
        return self.save

    @pyqtSlot()
    def handleOK(self):
        self.save = True

    @pyqtSlot()
    def handleCancel(self):
        self.save = False
