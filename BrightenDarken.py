from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, pyqtSlot, QAbstractTableModel, QModelIndex, QVariant
from PyQt5.QtGui import *

import cv2
import numpy as np
import qimage2ndarray

from BrightenDarkenValueTypeDialog import Ui_BrightenDarkenValueTypeDialog

class BrightenDarkenValueSelect(QDialog):
    def __init__(self):
    ##
        super(BrightenDarkenValueSelect, self).__init__()
        self.isChange = False
        self.initUI()
    ##
    
    def initUI(self):
        '''Initializes the GUI'''
        self.ui = Ui_BrightenDarkenValueTypeDialog()
        self.ui.setupUi(self)
        
        # Switch the default PyQt5 connectors to our class
        self.ui.buttonBox.accepted.connect(self.handleOK)
        self.ui.buttonBox.rejected.connect(self.handleCancel)
        
        QApplication.processEvents()
        
        self.show()
    
    @pyqtSlot()
    def handleOK(self):
        self.isChange = True
        self.close()
    
    @pyqtSlot()    
    def handleCancel(self):
        self.isChange = False
        self.close()

class BrightenDarken():
    def __init__(self, image):
        dialog = BrightenDarkenValueSelect()
        dialog.setModal(True)
        dialog.exec_()
        if dialog.isChange:
            self.process(image, dialog.ui.minDoubleSpinBoxPhi.value(), dialog.ui.minDoubleSpinBoxTheta.value())
            self.dialog = BeforeAfterHistogramDialog(image, self.afterImage)
            self.dialog.setModal(True)
            self.dialog.exec_()
    
    def getAfterQImage(self):
        return qimage2ndarray.array2qimage(self.afterImage)
        
    def isChanged(self):
        return self.dialog.isChange
    
    def process(self, image, phi, theta):
        maxIntensity = 255.0
        input = qimage2ndarray.rgb_view(image, 'little')
        
        b,g,r = cv2.split(input)

        imgB = (maxIntensity/phi)*(b/(maxIntensity/theta))**0.5
        imgG = (maxIntensity/phi)*(g/(maxIntensity/theta))**0.5
        imgR = (maxIntensity/phi)*(r/(maxIntensity/theta))**0.5
        
        imgB = np.array(imgB,dtype='uint8')
        imgG = np.array(imgG,dtype='uint8')
        imgR = np.array(imgR,dtype='uint8')
        
        img_out = cv2.merge((imgB, imgG, imgR))
        
        self.afterImage = cv2.cvtColor(img_out, cv2.COLOR_BGR2RGB)