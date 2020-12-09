import sys, random

from Binarization import *
from BrightenDarken import *
from ColorSelectDialogImpl import *
from Filtering import *
from GrayScale import GrayScale
from ImageOps import ImageOps
from JpegCompressionQualityDialogImpl import JpegCompressionQualityDialog

from MainWindow import Ui_MainWindow

import NetPbm
from MorphOp import MorphologicalOperations
from ThreeDeeCube import ThreeDeeCubeWindow


class UserGui(QMainWindow, Ui_MainWindow):
###
    def __init__(self):
    ## 
        super(UserGui, self).__init__()
        self.setupUi(self)
        self.isLoaded = False
        self.zoom = 1
        self.zoomTool = False
        self.initUI()
    ##
    
    def initUI(self):
        '''Initializes the GUI'''
    ##
        self.center()
        
        self.scene = QGraphicsScene()
        self.imageWidth = 0
        self.imageHeight = 0
        self.graphicsView.setMouseTracking(True)
        self.graphicsView.setCacheMode(QGraphicsView.CacheNone)
        self.graphicsView.setScene(self.scene)
        self.actionLoad.triggered.connect(self.openFile)
        self.actionSave.triggered.connect(self.saveFile)
        self.histogramPushButton.clicked.connect(self.showDefaultHistogram)
        self.equalizerPushButton.clicked.connect(self.equalize)
        self.brightenPushButton.clicked.connect(self.brighten)
        self.normalizePushButton.clicked.connect(self.normalize)
        self.otsuBinarizePushButton.clicked.connect(self.otsuBinarize)
        self.thresholdBinarizepushButton.clicked.connect(self.thresholdBinarize)
        self.niblackBinarizepushButton.clicked.connect(self.niblackBinarize)
        self.convolutePushButton.clicked.connect(self.convolute)
        self.kuwaharaPushButton.clicked.connect(self.kuwahara)
        self.medianFilterPushButton.clicked.connect(self.median)
        self.imageOpsPushButton.clicked.connect(self.imageOps)
        self.grayScalePushButton.clicked.connect(self.grayScale)
        self.customConvKernelPushButton.clicked.connect(self.customConvolute)
        self.bpbPushButton.clicked.connect(self.blackBinarize)
        self.morphOpsPushButton.clicked.connect(self.morphOps)
        
        self.scene.mouseMoveEvent = self.graphicsSceneMouseMoveEvent
        self.scene.mousePressEvent = self.graphicsSceneMousePressEvent
        
        QApplication.processEvents()
        
        self.show()
        
    ##
    
    def center(self):
        '''centers the window on the screen'''
    ##
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, 
            (screen.height()-size.height())/2)
    ##
    
    @pyqtSlot()
    def openFile(self):
        options = QFileDialog.Options()
        name, selFilter = QFileDialog.getOpenFileName(self, 'Open File', "", "Image file (*.png *.jpg *.jpeg *.bmp *.gif *.tif *.tiff);;PPM File (*.ppm);;All Files (*)", options = options)
        
        if name:
            if selFilter == "PPM File (*.ppm)":
                reader = NetPbm.NetPbmReader()
                ret = reader.fromFile(name)
                if ret != NetPbm.NetPbmReaderResult.OK:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Couldn't load PPM file!")
                    msg.setDetailedText("Reason: " + NetPbm.readerResultToString(ret))
                    msg.setWindowTitle("Error!")
                    msg.exec_()
                    return
                self.image = reader.getDecoded()
                self.fileName = name
                self.scene.clear()
                self.pixmap = QPixmap.fromImage(self.image)
                self.imageWidth, self.imageHeight = self.pixmap.width(), self.pixmap.height()
                self.internalPixmap = self.scene.addPixmap(self.pixmap)
                self.scene.setSceneRect(0, 0, self.imageWidth, self.imageHeight)
                self.isLoaded = True
            else:
                self.fileName = name
                self.scene.clear()
                self.image = QImage(name)
                self.pixmap = QPixmap.fromImage(self.image)
                self.imageWidth, self.imageHeight = self.pixmap.width(), self.pixmap.height()
                self.internalPixmap = self.scene.addPixmap(self.pixmap)
                self.scene.setSceneRect(0, 0, self.imageWidth, self.imageHeight)
                self.isLoaded = True
    
    @pyqtSlot()
    def saveFile(self):
        if self.isLoaded:
            name, selFilter = QFileDialog.getSaveFileName(self, "Save File", "", "PNG file (*.png);;JPEG file (*.jpg);;BMP file (*.bmp);;GIF file (*.gif);;TIFF file (*.tif);;PPM Binary File (*.ppm);;PPM ASCII File (*.ppm)")
        
            if name:
                if selFilter == "PPM Binary File (*.ppm)":
                    writer = NetPbm.NetPbmWriter()
                    ret = writer.save(self.image, name, NetPbm.NetPbmFileType.PortablePixMapBinary)
                    if ret != NetPbm.NetPbmWriterResult.OK:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Warning)
                        msg.setText("Couldn't save PPM file!")
                        msg.setDetailedText("Reason: " + NetPbm.writerResultToString(ret))
                        msg.setWindowTitle("Error!")
                        msg.exec_()
                elif selFilter == "PPM ASCII File (*.ppm)":
                    writer = NetPbm.NetPbmWriter()
                    ret = writer.save(self.image, name, NetPbm.NetPbmFileType.PortablePixMapAscii)
                    if ret != NetPbm.NetPbmWriterResult.OK:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Warning)
                        msg.setText("Couldn't save PPM file!")
                        msg.setDetailedText("Reason: " + NetPbm.writerResultToString(ret))
                        msg.setWindowTitle("Error!")
                        msg.exec_()
                elif selFilter == "JPEG file (*.jpg)":
                    dialog = JpegCompressionQualityDialog()
                    dialog.setModal(True)
                    dialog.exec_()
                    if dialog.getSave():
                        self.image.save(name, "jpeg", dialog.getValue())
                else:
                    self.image.save(name)
    
    @pyqtSlot()
    def showDefaultHistogram(self):
        if self.isLoaded:
            dialog = DefaultHistogramDialog(self.image)
            dialog.setModal(True)
            dialog.exec_()


    @pyqtSlot()
    def threeDeeCube(self):
        self.thirdDialog = ThreeDeeCubeWindow()

    @pyqtSlot()
    def equalize(self):
        if self.isLoaded:
            dialog = HistogramEqualizer(self.image)
            if dialog.isChanged():
                self.image = dialog.getAfterQImage()
                self.pixmap = QPixmap.fromImage(self.image)
                self.internalPixmap.setPixmap(self.pixmap)
                self.scene.update()
                self.graphicsView.update()
                QApplication.processEvents()
                
    @pyqtSlot()
    def normalize(self):
        if self.isLoaded:
            dialog = HistogramNormalize(self.image)
            if dialog.isChanged():
                self.image = dialog.getAfterQImage()
                self.pixmap = QPixmap.fromImage(self.image)
                self.internalPixmap.setPixmap(self.pixmap)
                self.scene.update()
                self.graphicsView.update()
                QApplication.processEvents()
    
    @pyqtSlot()
    def brighten(self):
        if self.isLoaded:
            dialog = BrightenDarken(self.image)
            if dialog.isChanged():
                self.image = dialog.getAfterQImage()
                self.pixmap = QPixmap.fromImage(self.image)
                self.internalPixmap.setPixmap(self.pixmap)
                self.scene.update()
                self.graphicsView.update()
                QApplication.processEvents()
                
    @pyqtSlot()
    def otsuBinarize(self):
        if self.isLoaded:
            dialog = OtsuBinarization(self.image)
            if dialog.isChanged():
                self.image = dialog.getAfterQImage()
                self.pixmap = QPixmap.fromImage(self.image)
                self.internalPixmap.setPixmap(self.pixmap)
                self.scene.update()
                self.graphicsView.update()
                QApplication.processEvents()
                
    @pyqtSlot()
    def thresholdBinarize(self):
        if self.isLoaded:
            dialog = HandPickedBinarization(self.image)
            if dialog.isChanged():
                self.image = dialog.getAfterQImage()
                self.pixmap = QPixmap.fromImage(self.image)
                self.internalPixmap.setPixmap(self.pixmap)
                self.scene.update()
                self.graphicsView.update()
                QApplication.processEvents()
    
    @pyqtSlot()
    def niblackBinarize(self):
        if self.isLoaded:
            dialog = NiblackBinarization(self.image)
            if dialog.isChanged():
                self.image = dialog.getAfterQImage()
                self.pixmap = QPixmap.fromImage(self.image)
                self.internalPixmap.setPixmap(self.pixmap)
                self.scene.update()
                self.graphicsView.update()
                QApplication.processEvents()
    
    @pyqtSlot()
    def convolute(self):
        if self.isLoaded:
            dialog = ConvoluteFiltering(self.image)
            if dialog.isChanged():
                self.image = dialog.getAfterQImage()
                self.pixmap = QPixmap.fromImage(self.image)
                self.internalPixmap.setPixmap(self.pixmap)
                self.scene.update()
                self.graphicsView.update()
                QApplication.processEvents()


    @pyqtSlot()
    def customConvolute(self):
        if self.isLoaded:
            dialog = CustomConvoluteFiltering(self.image)
            if dialog.isChanged():
                self.image = dialog.getAfterQImage()
                self.pixmap = QPixmap.fromImage(self.image)
                self.internalPixmap.setPixmap(self.pixmap)
                self.scene.update()
                self.graphicsView.update()
                QApplication.processEvents()
                
    @pyqtSlot()
    def kuwahara(self):
        if self.isLoaded:
            dialog = KuwaharaFiltering(self.image)
            if dialog.isChanged():
                self.image = dialog.getAfterQImage()
                self.pixmap = QPixmap.fromImage(self.image)
                self.internalPixmap.setPixmap(self.pixmap)
                self.scene.update()
                self.graphicsView.update()
                QApplication.processEvents()
                
    @pyqtSlot()
    def median(self):
        if self.isLoaded:
            dialog = MedianFiltering(self.image)
            if dialog.isChanged():
                self.image = dialog.getAfterQImage()
                self.pixmap = QPixmap.fromImage(self.image)
                self.internalPixmap.setPixmap(self.pixmap)
                self.scene.update()
                self.graphicsView.update()
                QApplication.processEvents()


    @pyqtSlot()
    def imageOps(self):
        if self.isLoaded:
            dialog = ImageOps(self.image)
            if dialog.isChanged():
                self.image = dialog.getAfterQImage()
                self.pixmap = QPixmap.fromImage(self.image)
                self.internalPixmap.setPixmap(self.pixmap)
                self.scene.update()
                self.graphicsView.update()
                QApplication.processEvents()


    @pyqtSlot()
    def grayScale(self):
        if self.isLoaded:
            dialog = GrayScale(self.image)
            if dialog.isChanged():
                self.image = dialog.getAfterQImage()
                self.pixmap = QPixmap.fromImage(self.image)
                self.internalPixmap.setPixmap(self.pixmap)
                self.scene.update()
                self.graphicsView.update()
                QApplication.processEvents()


    @pyqtSlot()
    def blackBinarize(self):
        if self.isLoaded:
            dialog = BlackPercentBinarization(self.image)
            if dialog.isChanged():
                self.image = dialog.getAfterQImage()
                self.pixmap = QPixmap.fromImage(self.image)
                self.internalPixmap.setPixmap(self.pixmap)
                self.scene.update()
                self.graphicsView.update()
                QApplication.processEvents()


    @pyqtSlot()
    def morphOps(self):
        if self.isLoaded:
            dialog = MorphologicalOperations(self.image)
            if dialog.isChanged():
                self.image = dialog.getAfterQImage()
                self.pixmap = QPixmap.fromImage(self.image)
                self.internalPixmap.setPixmap(self.pixmap)
                self.scene.update()
                self.graphicsView.update()
                QApplication.processEvents()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Equal or event.key() == Qt.Key_E:
            self.graphicsView.scale(1.2, 1.2)
        elif event.key() == Qt.Key_Minus or event.key() == Qt.Key_D:
            self.graphicsView.scale(1 / 1.2, 1 / 1.2)
            
    def graphicsSceneMouseMoveEvent(self, event):
        xPos = event.scenePos().x()
        yPos = event.scenePos().y()
        self.imgXVal.setText(str(xPos))
        self.imgYVal.setText(str(yPos))
        if xPos < 0 or yPos < 0 or xPos > self.imageWidth or yPos > self.imageHeight:
            self.imgXVal.setStyleSheet('QLabel { color : red; }')
            self.imgYVal.setStyleSheet('QLabel { color : red; }')
        else:
            self.imgXVal.setStyleSheet('QLabel { color : black; }')
            self.imgYVal.setStyleSheet('QLabel { color : black; }')
            if self.isLoaded:
                c = self.image.pixel(xPos, yPos)
                cRGB = QColor(c).getRgb()
                self.imgRVal.setText(str(cRGB[0]))
                self.imgGVal.setText(str(cRGB[1]))
                self.imgBVal.setText(str(cRGB[2]))
            
    def graphicsSceneMousePressEvent(self, event):
        if self.isLoaded: 
            xPos = event.scenePos().x()
            yPos = event.scenePos().y()
            c = self.image.pixel(xPos, yPos)
            cRGB = QColor(c).getRgb()
            dialog = ColorSelectDialog(cRGB)
            dialog.setModal(True)
            dialog.exec_()
            if dialog.isChange:
                newColor = dialog.getValue()
                ## Note: This is slow, for processing larger amount of pixels, use numpy
                ## or manipulate directly via SIP uint pointer wrapper
                self.image.setPixel(xPos, yPos, newColor)
                self.pixmap = QPixmap.fromImage(self.image)
                self.internalPixmap.setPixmap(self.pixmap)
                self.scene.update()
                self.graphicsView.update()
                QApplication.processEvents()
    

    
if __name__ == '__main__':
    app = QApplication([])
    gui = UserGui()    
    sys.exit(app.exec_())