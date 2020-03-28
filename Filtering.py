from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, pyqtSlot, QAbstractTableModel, QModelIndex, QVariant
from PyQt5.QtGui import *

import cv2
import numpy as np
import qimage2ndarray
from skimage.exposure import rescale_intensity
from scipy.signal import convolve2d

from HistogramUtility import *

from ConvoluteKernelDialog import *
from KuwaharaWindowDialog import *
from MedianSizeDialog import *

#############################
### CONVOLUTION FILTERING ###
#############################

class ConvoluteKernelDialog(QDialog):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_ConvoluteKernelDialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.handleOK)
        self.ui.buttonBox.rejected.connect(self.handleCancel)
        
        # Kernels
        self.blurKernel = np.ones((3, 3), dtype="int") * (1.0 / (3 * 3))
        
        self.sharpenKernel = np.array((
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]), dtype="int")
            
        self.laplaceKernel = np.array((
            [0, 1, 0],
            [1, -4, 1],
            [0, 1, 0]), dtype="int")

        self.sobelXKernel = np.array((
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1]), dtype="int")

        self.sobelYKernel = np.array((
            [-1, -2, -1],
            [0, 0, 0],
            [1, 2, 1]), dtype="int")
            
        self.prewittKernel = np.array((
            [-1, 0, 1],
            [-1, 0, 1],
            [-1, 0, 1]), dtype="int")
        
        self.ui.comboBox.activated[str].connect(self.onKernelTypeChange)
        
        self.onKernelTypeChange()
        
        
    def getKernel(self):
        if self.ui.comboBox.currentText() == "Blur":
            return np.ones((3, 3), dtype="float") * (1.0 / (3 * 3))
        else:
            return np.array((
                [self.ui.kernelValueSpinBox1x1.value(), self.ui.kernelValueSpinBox1x2.value(), self.ui.kernelValueSpinBox1x3.value()],
                [self.ui.kernelValueSpinBox2x1.value(), self.ui.kernelValueSpinBox2x2.value(), self.ui.kernelValueSpinBox2x3.value()],
                [self.ui.kernelValueSpinBox3x1.value(), self.ui.kernelValueSpinBox3x2.value(), self.ui.kernelValueSpinBox3x3.value()]), dtype="int")
    
    def getIfChanged(self):
        return self.isChange
    
    @pyqtSlot()
    def handleOK(self):
        self.isChange = True

    @pyqtSlot()    
    def handleCancel(self):
        self.isChange = False
        
    @pyqtSlot()
    def onKernelTypeChange(self):
        kernelToChange = self.sharpenKernel
        if self.ui.comboBox.currentText() == "Blur":
            kernelToChange = self.blurKernel
        elif self.ui.comboBox.currentText() == "Prewitt":
            kernelToChange = self.prewittKernel
        elif self.ui.comboBox.currentText() == "SobelX":
            kernelToChange = self.sobelXKernel
        elif self.ui.comboBox.currentText() == "SobelY":
            kernelToChange = self.sobelYKernel
        elif self.ui.comboBox.currentText() == "Laplace":
            kernelToChange = self.laplaceKernel
        elif self.ui.comboBox.currentText() == "Sharpen":
            kernelToChange = self.sharpenKernel
        else:
            print("nothing to change")
            return
            
        self.ui.kernelValueSpinBox1x1.setValue(kernelToChange[0][0])
        self.ui.kernelValueSpinBox1x2.setValue(kernelToChange[0][1])
        self.ui.kernelValueSpinBox1x3.setValue(kernelToChange[0][2])
        self.ui.kernelValueSpinBox2x1.setValue(kernelToChange[1][0])
        self.ui.kernelValueSpinBox2x2.setValue(kernelToChange[1][1])
        self.ui.kernelValueSpinBox2x3.setValue(kernelToChange[1][2])
        self.ui.kernelValueSpinBox3x1.setValue(kernelToChange[2][0])
        self.ui.kernelValueSpinBox3x2.setValue(kernelToChange[2][1])
        self.ui.kernelValueSpinBox3x3.setValue(kernelToChange[2][2])

class ConvoluteFiltering():
    def __init__(self, image):
        self.dialog = ConvoluteKernelDialog()
        self.dialog.setModal(True)
        self.dialog.exec_()
        if self.dialog.getIfChanged():
            self.process(image, self.dialog.getKernel())
            showInput = cv2.cvtColor(cv2.cvtColor(qimage2ndarray.rgb_view(image, 'little'), cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
            self.dialog = BeforeAfterHistogramDialog(qimage2ndarray.array2qimage(showInput), self.afterImage)
            self.dialog.setModal(True)
            self.dialog.exec_()
    
    def getAfterQImage(self):
        return qimage2ndarray.array2qimage(self.afterImage)
        
    def isChanged(self):
        return self.dialog.isChange
    
    def process(self, image, kernel):
        ## Convert RGB QImage to BGR OpenCV/numpy Image and that to gray scale.
        input = qimage2ndarray.rgb_view(image, 'little')
        grayImage = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
        
        ## get kernel and image values
        (imageHeight, imageWidth) = grayImage.shape[:2]
        (kernelHeight, kernelWidth) = kernel.shape[:2]
        
        ## reshape the input to have the padding and create empty final image.
        padding = (kernelWidth - 1) // 2
        grayImage = cv2.copyMakeBorder(grayImage, padding, padding, padding, padding,
            cv2.BORDER_REPLICATE)
        finalImage = np.zeros((imageHeight, imageWidth), dtype="float32")
        
        ## start computing filtered values
        for y in np.arange(padding, imageHeight + padding):
            for x in np.arange(padding, imageWidth + padding):
                regionOfInterest = grayImage[y - padding:y + padding + 1, x - padding:x + padding + 1]
                pixelValue = (regionOfInterest * kernel).sum()
                finalImage[y - padding, x - padding] = pixelValue
        
        ## post-process the image (mainly to convert float values back to int)
        finalImage = rescale_intensity(finalImage, in_range=(0, 255))
        finalImage = (finalImage * 255).astype("uint8")
        
        ## Convert the Gray image to color for histogram and main window
        self.afterImage = cv2.cvtColor(finalImage, cv2.COLOR_GRAY2BGR)




################
### KUWAHARA ###
################

class KuwaharaWindowDialog(QDialog):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_KuwaharaWindowDialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.handleOK)
        self.ui.buttonBox.rejected.connect(self.handleCancel)
        self.ui.spinBox.valueChanged.connect(self.onNWindowValueChange)
        self.ui.valueLabel.setText("{}".format(4 * self.ui.spinBox.value() + 1))
        
    def getWindowSize(self):
        return 4 * self.ui.spinBox.value() + 1
    
    def getIfChanged(self):
        return self.isChange
    
    @pyqtSlot()
    def handleOK(self):
        self.isChange = True

    @pyqtSlot()    
    def handleCancel(self):
        self.isChange = False
        
    @pyqtSlot()
    def onNWindowValueChange(self):
         self.ui.valueLabel.setText("{}".format(4 * self.ui.spinBox.value() + 1))
         
         
class KuwaharaFiltering():
    def __init__(self, image):
        self.dialog = KuwaharaWindowDialog()
        self.dialog.setModal(True)
        self.dialog.exec_()
        if self.dialog.getIfChanged():
            print(self.dialog.getWindowSize())
            self.process(image, self.dialog.getWindowSize())
            showInput = cv2.cvtColor(cv2.cvtColor(qimage2ndarray.rgb_view(image, 'little'), cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
            self.dialog = BeforeAfterHistogramDialog(qimage2ndarray.array2qimage(showInput), self.afterImage)
            self.dialog.setModal(True)
            self.dialog.exec_()
    
    def getAfterQImage(self):
        return qimage2ndarray.array2qimage(self.afterImage)
        
    def isChanged(self):
        return self.dialog.isChange
    
    def process(self, image, windowSize):
        ## Convert RGB QImage to BGR OpenCV/numpy Image and that to gray scale.
        input = qimage2ndarray.rgb_view(image, 'little')
        grayImage = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
        
        grayImageFloat = grayImage.astype(np.float64)
        
        averageKernelRow = np.hstack((np.ones((1,(windowSize-1)//2+1)),np.zeros((1,(windowSize-1)//2))))
        adderForKern = np.zeros((1,windowSize))
        temporaryKernel = np.tile(averageKernelRow, ((windowSize-1)//2+1,1))
        temporaryKernel = np.vstack((temporaryKernel, np.tile(adderForKern, ((windowSize-1)//2,1))))
        temporaryKernel = temporaryKernel/np.sum(temporaryKernel)
        
        kernel = np.empty((4,windowSize,windowSize))
        kernel[0] = temporaryKernel			# North-west (a)
        kernel[1] = np.fliplr(temporaryKernel)	# North-east (b)
        kernel[2] = np.flipud(temporaryKernel)	# South-west (c)
        kernel[3] = np.fliplr(kernel[2])	# South-east (d)
        
        squaredImage = grayImageFloat**2
	
        # preallocate these arrays to make it apparently %15 faster
        averages = np.zeros([4, grayImageFloat.shape[0], grayImageFloat.shape[1]])
        standardDeviation = averages.copy()
        
        for k in range(4):
            averages[k] = convolve2d(grayImageFloat, kernel[k], mode='same')
        standardDeviation[k] = convolve2d(squaredImage, kernel[k], mode='same')
        standardDeviation[k] = standardDeviation[k]-averages[k]**2
        
        indices = np.argmin(standardDeviation, 0) 


        filtered = np.zeros(grayImage.shape)
        for row in range(grayImage.shape[0]):
            for col in range(grayImage.shape[1]):
                filtered[row,col] = averages[indices[row,col], row,col]
        
        finalImage = filtered.astype(np.uint8)
        
        ## Convert the Gray image to color for histogram and main window
        self.afterImage = cv2.cvtColor(finalImage, cv2.COLOR_GRAY2BGR)


class MedianSizeDialog(QDialog):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_MedianSizeDialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.handleOK)
        self.ui.buttonBox.rejected.connect(self.handleCancel)
        self.ui.spinBox.valueChanged.connect(self.onNWindowValueChange)
        self.ui.filterSizeLabel.setText("{}".format(self.ui.spinBox.value()))
    
    def getWindowSize(self):
        return self.ui.spinBox.value()
        
    def getIfChanged(self):
        return self.isChange

    @pyqtSlot()
    def handleOK(self):
        self.isChange = True
        
    @pyqtSlot()
    def handleCancel(self):
        self.isChange = False

    @pyqtSlot()
    def onNWindowValueChange(self):
        self.ui.filterSizeLabel.setText("{}x{}".format(self.ui.spinBox.value(), self.ui.spinBox.value()))

class MedianFiltering():
    def __init__(self, image):
        self.dialog = MedianSizeDialog()
        self.dialog.setModal(True)
        self.dialog.exec_()
        if self.dialog.getIfChanged():
            self.process(image, self.dialog.getWindowSize())
            showInput = cv2.cvtColor(cv2.cvtColor(qimage2ndarray.rgb_view(image, 'little'), cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
            self.dialog = BeforeAfterHistogramDialog(qimage2ndarray.array2qimage(showInput), self.afterImage)
            self.dialog.setModal(True)
            self.dialog.exec_()
    
    def getAfterQImage(self):
        return qimage2ndarray.array2qimage(self.afterImage)
        
    def isChanged(self):
        return self.dialog.isChange
    
    def process(self, image, windowSize):
        ## Convert RGB QImage to BGR OpenCV/numpy Image and that to gray scale.
        input = qimage2ndarray.rgb_view(image, 'little')
        grayImage = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
        
        temp = []
        indexer = windowSize // 2
        window = [
            (i, j)
            for i in range(-indexer, windowSize-indexer)
            for j in range(-indexer, windowSize-indexer)
        ]
        
        print(window)
        
        index = len(window) // 2
        for i in range(len(grayImage)):
            for j in range(len(grayImage[0])):
                grayImage[i][j] = sorted(
                    0 if (
                        min(i+a, j+b) < 0
                        or len(grayImage) <= i+a
                        or len(grayImage[0]) <= j+b
                    ) else grayImage[i+a][j+b]
                    for a, b in window
                )[index]
        
        ## Convert the Gray image to color for histogram and main window
        self.afterImage = cv2.cvtColor(grayImage, cv2.COLOR_GRAY2BGR)
