from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, pyqtSlot, QAbstractTableModel, QModelIndex, QVariant
from PyQt5.QtGui import *

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure

import cv2
import numpy as np
import qimage2ndarray

from HistogramWidget import HistogramWidget
from BeforeAfterHistogramDialog import Ui_BeforeAfterHistogramDialog
from DefaultHistogramDialog import Ui_DefaultHistogramDialog

class BeforeAfterHistogramDialog(QDialog):
    def __init__(self, imgBeforePath, imgAfter):
        QWidget.__init__(self)
        self.ui = Ui_BeforeAfterHistogramDialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Results")
        self.ui.beforeImageLabel.setScaledContents(True)
        self.ui.afterImageLabel.setScaledContents(True)
        self.ui.buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.handleApply)
        self.ui.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.handleCancel)
        self.displayHistogram(imgBeforePath, imgAfter)
        self.isChange = False
        
    def displayHistogram(self, imgBefore, imgAfter):
        
        self.ui.beforeHistogramWidget.canvas.sumbu1.clear()
        self.ui.afterHistogramWidget.canvas.sumbu1.clear()
        readBefore = qimage2ndarray.rgb_view(imgBefore, 'little')
        color = ('b','g','r')
        for i,col in enumerate(color):
            histr = cv2.calcHist([readBefore],[i],None,[256],[0,256])
            self.ui.beforeHistogramWidget.canvas.sumbu1.plot(histr,color = col,linewidth=3.0)
            self.ui.beforeHistogramWidget.canvas.sumbu1.set_ylabel('Number Of values', color='blue')
            self.ui.beforeHistogramWidget.canvas.sumbu1.set_xlabel('Pixel Value', color='blue')
            self.ui.beforeHistogramWidget.canvas.sumbu1.set_facecolor('xkcd:wheat')
            self.ui.beforeHistogramWidget.canvas.sumbu1.grid()
        self.ui.beforeHistogramWidget.canvas.draw()
        self.ui.beforeImageLabel.setPixmap(QPixmap(imgBefore))
        
        # Read after Image
        
        im_bgr = cv2.cvtColor(imgAfter, cv2.COLOR_RGB2BGR)
        
        for i,col in enumerate(color):
            histr = cv2.calcHist([im_bgr],[i],None,[256],[0,256])
            self.ui.afterHistogramWidget.canvas.sumbu1.plot(histr,color = col,linewidth=3.0)
            self.ui.afterHistogramWidget.canvas.sumbu1.set_ylabel('Number Of values', color='blue')
            self.ui.afterHistogramWidget.canvas.sumbu1.set_xlabel('Pixel Value', color='blue')
            self.ui.afterHistogramWidget.canvas.sumbu1.set_facecolor('xkcd:wheat')
            self.ui.afterHistogramWidget.canvas.sumbu1.grid()
        self.ui.afterHistogramWidget.canvas.draw()
        converted = qimage2ndarray.array2qimage(imgAfter)
        self.ui.afterImageLabel.setPixmap(QPixmap(converted))
        
    @pyqtSlot()
    def handleApply(self):
        self.isChange = True
        print("Will Change!")
        self.close()
    
    @pyqtSlot()    
    def handleCancel(self):
        self.isChange = False
        self.close()
    
class DefaultHistogramDialog(QDialog):
    def __init__(self, imgPath):
        QWidget.__init__(self)
        self.ui = Ui_DefaultHistogramDialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Histogram")
        self.ui.pushButton.clicked.connect(self.handleClose) 
        self.displayHistogram(imgPath)
    
    def displayHistogram(self, fileName):
        
        self.ui.widget.canvas.sumbu1.clear()
        read_img = qimage2ndarray.rgb_view(fileName, 'little')
        b, g, r = cv2.split(read_img)
        split = np.array([b.flatten(), g.flatten(), r.flatten()])
        color = ('b','g','r')
        for i,col in enumerate(color):
            histr = np.bincount(split[i], minlength=256).reshape(256, 1)
            self.ui.widget.canvas.sumbu1.plot(histr,color = col,linewidth=3.0)
            self.ui.widget.canvas.sumbu1.set_ylabel('Number Of values', color='blue')
            self.ui.widget.canvas.sumbu1.set_xlabel('Pixel Value', color='blue')
            self.ui.widget.canvas.sumbu1.set_facecolor('xkcd:wheat')
            self.ui.widget.canvas.sumbu1.grid()
        self.ui.widget.canvas.draw()
    
    @pyqtSlot()
    def handleClose(self):
        self.close()
        
        
############################
### HISTOGRAM PROCESSING ###
############################

## aka wyrównywanie obrazu
class HistogramEqualizer():
    def __init__(self, image):
        self.process(image)
        self.dialog = BeforeAfterHistogramDialog(image, self.afterImage)
        self.dialog.setModal(True)
        self.dialog.exec_()
    
    def getAfterQImage(self):
        return qimage2ndarray.array2qimage(self.afterImage)
        
    def isChanged(self):
        return self.dialog.isChange
    
    def process(self, image):
        input = qimage2ndarray.rgb_view(image, 'little')
        
        b,g,r = cv2.split(input)
        histB = np.bincount(b.flatten(), minlength=256)
        histG = np.bincount(g.flatten(), minlength=256)
        histR = np.bincount(r.flatten(), minlength=256)

        cdfB = np.cumsum(histB)  
        cdfG = np.cumsum(histG)
        cdfR = np.cumsum(histR)
    
        cdfMaskedBinary = np.ma.masked_equal(cdfB,0)
        cdfMaskedBinary = (cdfMaskedBinary - cdfMaskedBinary.min())*255/(cdfMaskedBinary.max()-cdfMaskedBinary.min())
        cdfMaskedFinalBlue = np.ma.filled(cdfMaskedBinary,0).astype('uint8')
  
        cdfMaskedGreen = np.ma.masked_equal(cdfG,0)
        cdfMaskedGreen = (cdfMaskedGreen - cdfMaskedGreen.min())*255/(cdfMaskedGreen.max()-cdfMaskedGreen.min())
        cdfMaskedFinalGreen = np.ma.filled(cdfMaskedGreen,0).astype('uint8')
        cdfMaskedRed = np.ma.masked_equal(cdfR,0)
        cdfMaskedRed = (cdfMaskedRed - cdfMaskedRed.min())*255/(cdfMaskedRed.max()-cdfMaskedRed.min())
        cdfMaskedFinalRed = np.ma.filled(cdfMaskedRed,0).astype('uint8')

        imgB = cdfMaskedFinalBlue[b]
        imgG = cdfMaskedFinalGreen[g]
        imgR = cdfMaskedFinalRed[r]
  
        img_out = cv2.merge((imgB, imgG, imgR))
        
        self.afterImage = cv2.cvtColor(img_out, cv2.COLOR_BGR2RGB)

# aka rozciąganie obrazu
class HistogramNormalize():
    def __init__(self, image):
        self.process(image)
        self.dialog = BeforeAfterHistogramDialog(image, self.afterImage)
        self.dialog.setModal(True)
        self.dialog.exec_()
    
    def getAfterQImage(self):
        return qimage2ndarray.array2qimage(self.afterImage)
        
    def isChanged(self):
        return self.dialog.isChange

    def getMinMax(self, channel):
        hist = np.bincount(channel.flatten(), minlength=256)
        valid = np.where(hist != 0)[0]
        min = valid[hist[valid].argmin()]
        max = hist.argmax()
        if min > max:
            return max, min
        return min, max

    def process(self, image):
        input = qimage2ndarray.rgb_view(image, 'little')
        
        b,g,r = cv2.split(input)
        minB, maxB = self.getMinMax(b)
        minG, maxG = self.getMinMax(g)
        minR, maxR = self.getMinMax(r)
        minO = 0
        maxO = 255

        tmpB = (((b - minB) / (maxB - minB)) * 256)
        tmpG = (((g - minG) / (maxG - minG)) * 256)
        tmpR = (((r - minR) / (maxR - minR)) * 256)
        #tmpB = (b-minB)*(((maxO-minO)/(maxB-minB))+minO)
        #tmpG = (g - minG) * (((maxO - minO) / (maxG - minG)) + minO)
        #tmpR = (g - minR) * (((maxO - minO) / (maxR - minR)) + minO)
        imgB = np.where(tmpB >= 255, 255, tmpB)
        imgG = np.where(tmpG >= 255, 255, tmpG)
        imgR = np.where(tmpG >= 255, 255, tmpR)


        #imgB = (((b - minB) / (maxB - minB))).astype('uint8')
        #imgG = (((g - minG) / (maxG - minG))).astype('uint8')
        #imgR = (((r - minR) / (maxR - minR))).astype('uint8')
  
        img_out = cv2.merge((imgB.astype("uint8"), imgG.astype("uint8"), imgR.astype("uint8")))
        
        self.afterImage = cv2.cvtColor(img_out, cv2.COLOR_BGR2RGB)

    