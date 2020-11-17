from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, pyqtSlot, QAbstractTableModel, QModelIndex, QVariant
from PyQt5.QtGui import *

import cv2
import numpy as np
import qimage2ndarray

from BlackBinarizationDialog import Ui_BlackBinarizationValueDialog
from HistogramUtility import *

from BinarizationValueSelectDialog import Ui_BinarizationValueSelectDialog
from NiblackBinarizationValueSelectDialog import Ui_NiblackBinarizationValueSelectDialog

class HandPickedBinarizationThresholdValueSelectDialog(QDialog):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_BinarizationValueSelectDialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.handleOK)
        self.ui.buttonBox.rejected.connect(self.handleCancel)
        
    def getValue(self):
        return self.ui.spinBox.value()
    
    def getIfChanged(self):
        return self.isChange
    
    @pyqtSlot()
    def handleOK(self):
        self.isChange = True

    @pyqtSlot()    
    def handleCancel(self):
        self.isChange = False

class NiblackBinarizationThresholdValueSelectDialog(QDialog):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_NiblackBinarizationValueSelectDialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.handleOK)
        self.ui.buttonBox.rejected.connect(self.handleCancel)
        
    def getLocalWindow(self):
        return self.ui.localWindowSpinBox.value()
    
    def getLocalThreshold(self):
        return self.ui.localThresholdDoubleSpinBox.value()
        
    def getGlobalThreshold(self):
        return self.ui.globalThresholdSpinBox.value()
    
    def getIfChanged(self):
        return self.isChange
    
    @pyqtSlot()
    def handleOK(self):
        self.isChange = True

    @pyqtSlot()    
    def handleCancel(self):
        self.isChange = False

class HandPickedBinarization():
    def __init__(self, image):
        self.dialog = HandPickedBinarizationThresholdValueSelectDialog()
        self.dialog.setModal(True)
        self.dialog.exec_()
        if self.dialog.getIfChanged():
            self.process(image, self.dialog.getValue())
            showInput = cv2.cvtColor(cv2.cvtColor(qimage2ndarray.rgb_view(image, 'little'), cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
            self.dialog = BeforeAfterHistogramDialog(qimage2ndarray.array2qimage(showInput), self.afterImage)
            self.dialog.setModal(True)
            self.dialog.exec_()
    
    def getAfterQImage(self):
        return qimage2ndarray.array2qimage(self.afterImage)
        
    def isChanged(self):
        return self.dialog.isChange
    
    def process(self, image, threshold):
        ## Convert RGB QImage to BGR OpenCV/numpy Image and that to gray scale.
        input = qimage2ndarray.rgb_view(image, 'little')
        grayImage = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
        
        ## perform binarization
        finalImage = grayImage.copy()
        finalImage[grayImage > threshold] = 255
        finalImage[grayImage < threshold] = 0
        
        ## Convert the Gray image to color for histogram and main window
        self.afterImage = cv2.cvtColor(finalImage, cv2.COLOR_GRAY2BGR)


class BlackBinarizationPercentValueSelectDialog(QDialog):
    def __init__(self):
        QWidget.__init__(self)
        self.isChange = False
        self.ui = Ui_BlackBinarizationValueDialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.handleOK)
        self.ui.buttonBox.rejected.connect(self.handleCancel)

    def getIfChanged(self):
        return self.isChange

    @pyqtSlot()
    def handleOK(self):
        self.isChange = True

    @pyqtSlot()
    def handleCancel(self):
        self.isChange = False

    def getPercent(self):
        return self.ui.horizontalSlider.value()


class BlackPercentBinarization:
    def __init__(self, image):
        self.dialog = BlackBinarizationPercentValueSelectDialog()
        self.dialog.setModal(True)
        self.dialog.exec_()
        if self.dialog.getIfChanged():
            self.process(image, self.dialog.getPercent())
            showInput = cv2.cvtColor(cv2.cvtColor(qimage2ndarray.rgb_view(image, 'little'), cv2.COLOR_BGR2GRAY),
                                     cv2.COLOR_GRAY2BGR)
            self.dialog = BeforeAfterHistogramDialog(qimage2ndarray.array2qimage(showInput), self.afterImage)
            self.dialog.setModal(True)
            self.dialog.exec_()

    def getAfterQImage(self):
        return qimage2ndarray.array2qimage(self.afterImage)

    def isChanged(self):
        return self.dialog.isChange

    def process(self, image, percent):
        ## Convert RGB QImage to BGR OpenCV/numpy Image and that to gray scale.
        input = qimage2ndarray.rgb_view(image, 'little')
        grayImage = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
        all = np.bincount(grayImage.flatten(), minlength=256)
        lut = np.zeros((256))
        limes = ((percent / 100) * all.sum()).astype(int)
        nextsum = 0
        for i in range(len(lut)):
            nextsum += all[i]
            if nextsum < limes:
                lut[i] = 0
            else:
                lut[i] = 255


        ## perform binarization
        finalImage = grayImage.copy()
        for i in range(len(lut)):
            finalImage[grayImage == i] = lut[i]

        ## Convert the Gray image to color for histogram and main window
        self.afterImage = cv2.cvtColor(finalImage, cv2.COLOR_GRAY2BGR)

class NiblackBinarization():
    def __init__(self, image):
        self.dialog = NiblackBinarizationThresholdValueSelectDialog()
        self.dialog.setModal(True)
        self.dialog.exec_()
        if self.dialog.getIfChanged():
            self.process(image, self.dialog.getLocalWindow(), self.dialog.getLocalThreshold(), self.dialog.getGlobalThreshold())
            showInput = cv2.cvtColor(cv2.cvtColor(qimage2ndarray.rgb_view(image, 'little'), cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
            self.dialog = BeforeAfterHistogramDialog(qimage2ndarray.array2qimage(showInput), self.afterImage)
            self.dialog.setModal(True)
            self.dialog.exec_()
    
    def getAfterQImage(self):
        return qimage2ndarray.array2qimage(self.afterImage)
        
    def isChanged(self):
        return self.dialog.isChange
    
    def process(self, image, localWindow, localThreshold, globalThreshold):
        # Convert RGB QImage to BGR OpenCV/numpy Image and that to gray scale.
        input = qimage2ndarray.rgb_view(image, 'little')
        grayImage = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
        
        imageRows, imageColums = grayImage.shape
        helperArrRows, helperArrColums = imageRows + 1, imageColums + 1

        integralImage = np.zeros((helperArrRows, helperArrColums), np.float)
        integralImageSquared = np.zeros((helperArrRows, helperArrColums), np.float)

        integralImage[1:, 1:] = np.cumsum(np.cumsum(grayImage.astype(np.float), axis=0), axis=1)
        integralImageSquared[1:, 1:] = np.cumsum(np.cumsum(np.square(grayImage.astype(np.float)), axis=0), axis=1)

        x, y = np.meshgrid(np.arange(1, helperArrColums), np.arange(1, helperArrRows))

        localCoordSize = localWindow // 2
        x1 = (x - localCoordSize).clip(1, imageColums)
        x2 = (x + localCoordSize).clip(1, imageColums)
        y1 = (y - localCoordSize).clip(1, imageRows)
        y2 = (y + localCoordSize).clip(1, imageRows)

        localAreaSize = (y2 - y1 + 1) * (x2 - x1 + 1)

        sums = (integralImage[y2, x2] - integralImage[y2, x1 - 1] -
                integralImage[y1 - 1, x2] + integralImage[y1 - 1, x1 - 1])
        sumsSquared = (integralImageSquared[y2, x2] - integralImageSquared[y2, x1 - 1] -
                    integralImageSquared[y1 - 1, x2] + integralImageSquared[y1 - 1, x1 - 1])

        means = sums / localAreaSize

        localStandardDeviation = np.sqrt(sumsSquared / localAreaSize - np.square(means))

        thresholds = means + localThreshold * localStandardDeviation

        finalImage = grayImage.copy()
        finalImage = ((finalImage >= thresholds) * 255).astype(np.uint8)
        
        # Convert the Gray image to color for histogram and main window
        self.afterImage = cv2.cvtColor(finalImage, cv2.COLOR_GRAY2BGR)

class OtsuBinarization():
    def __init__(self, image):
        self.process(image)
        showInput = cv2.cvtColor(cv2.cvtColor(qimage2ndarray.rgb_view(image, 'little'), cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
        self.dialog = BeforeAfterHistogramDialog(qimage2ndarray.array2qimage(showInput), self.afterImage)
        self.dialog.setModal(True)
        self.dialog.exec_()
    
    def getAfterQImage(self):
        return qimage2ndarray.array2qimage(self.afterImage)
        
    def isChanged(self):
        return self.dialog.isChange
    
    def process(self, image):
        
        ## Convert RGB QImage to BGR OpenCV/numpy Image and that to gray scale.
        input = qimage2ndarray.rgb_view(image, 'little')
        grayImage = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
        
        pixelNum = grayImage.shape[0] * grayImage.shape[1]
        meanWeight = 1.0/pixelNum
        his, bins = np.histogram(grayImage, np.arange(0,257))
        
        finalThreshold = -1
        finalColorValue = -1
        intensities = np.arange(256)
        
        ## compute final threshold
        for t in bins[1:-1]:
            pcb = np.sum(his[:t])
            pcf = np.sum(his[t:])
            Wb = pcb * meanWeight
            Wf = pcf * meanWeight

            mub = np.sum(intensities[:t]*his[:t]) / float(pcb)
            muf = np.sum(intensities[t:]*his[t:]) / float(pcf)
            
            ## calculate final minimization value
            value = Wb * Wf * (mub - muf) ** 2

            if value > finalColorValue:
                finalThreshold = t
                finalColorValue = value
        
        ## perform binarization
        finalImage = grayImage.copy()
        print(finalThreshold)
        finalImage[grayImage > finalThreshold] = 255
        finalImage[grayImage < finalThreshold] = 0
        
        ## Convert the Gray image to color for histogram and main window
        self.afterImage = cv2.cvtColor(finalImage, cv2.COLOR_GRAY2BGR)

    
