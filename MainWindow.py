# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(10, 10, 641, 461))
        self.graphicsView.setObjectName("graphicsView")
        self.imgXKey = QtWidgets.QLabel(self.centralwidget)
        self.imgXKey.setGeometry(QtCore.QRect(10, 480, 21, 16))
        self.imgXKey.setObjectName("imgXKey")
        self.imgYKey = QtWidgets.QLabel(self.centralwidget)
        self.imgYKey.setGeometry(QtCore.QRect(10, 500, 21, 16))
        self.imgYKey.setObjectName("imgYKey")
        self.imgRKey = QtWidgets.QLabel(self.centralwidget)
        self.imgRKey.setGeometry(QtCore.QRect(130, 480, 21, 16))
        self.imgRKey.setObjectName("imgRKey")
        self.imgGKey = QtWidgets.QLabel(self.centralwidget)
        self.imgGKey.setGeometry(QtCore.QRect(130, 500, 21, 16))
        self.imgGKey.setObjectName("imgGKey")
        self.imgBKey = QtWidgets.QLabel(self.centralwidget)
        self.imgBKey.setGeometry(QtCore.QRect(130, 520, 21, 16))
        self.imgBKey.setObjectName("imgBKey")
        self.imgXVal = QtWidgets.QLabel(self.centralwidget)
        self.imgXVal.setGeometry(QtCore.QRect(30, 480, 91, 16))
        self.imgXVal.setText("")
        self.imgXVal.setObjectName("imgXVal")
        self.imgYVal = QtWidgets.QLabel(self.centralwidget)
        self.imgYVal.setGeometry(QtCore.QRect(30, 500, 91, 16))
        self.imgYVal.setText("")
        self.imgYVal.setObjectName("imgYVal")
        self.imgRVal = QtWidgets.QLabel(self.centralwidget)
        self.imgRVal.setGeometry(QtCore.QRect(150, 480, 91, 16))
        self.imgRVal.setText("")
        self.imgRVal.setObjectName("imgRVal")
        self.imgGVal = QtWidgets.QLabel(self.centralwidget)
        self.imgGVal.setGeometry(QtCore.QRect(150, 500, 91, 16))
        self.imgGVal.setText("")
        self.imgGVal.setObjectName("imgGVal")
        self.imgBVal = QtWidgets.QLabel(self.centralwidget)
        self.imgBVal.setGeometry(QtCore.QRect(160, 520, 91, 16))
        self.imgBVal.setText("")
        self.imgBVal.setObjectName("imgBVal")
        self.histogramPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.histogramPushButton.setGeometry(QtCore.QRect(666, 12, 121, 21))
        self.histogramPushButton.setObjectName("histogramPushButton")
        self.equalizerPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.equalizerPushButton.setGeometry(QtCore.QRect(666, 40, 121, 23))
        self.equalizerPushButton.setObjectName("equalizerPushButton")
        self.brightenPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.brightenPushButton.setGeometry(QtCore.QRect(666, 100, 121, 23))
        self.brightenPushButton.setObjectName("brightenPushButton")
        self.normalizePushButton = QtWidgets.QPushButton(self.centralwidget)
        self.normalizePushButton.setGeometry(QtCore.QRect(666, 70, 121, 23))
        self.normalizePushButton.setObjectName("normalizePushButton")
        self.otsuBinarizePushButton = QtWidgets.QPushButton(self.centralwidget)
        self.otsuBinarizePushButton.setGeometry(QtCore.QRect(666, 130, 121, 23))
        self.otsuBinarizePushButton.setObjectName("otsuBinarizePushButton")
        self.niblackBinarizepushButton = QtWidgets.QPushButton(self.centralwidget)
        self.niblackBinarizepushButton.setGeometry(QtCore.QRect(667, 160, 121, 23))
        self.niblackBinarizepushButton.setObjectName("niblackBinarizepushButton")
        self.thresholdBinarizepushButton = QtWidgets.QPushButton(self.centralwidget)
        self.thresholdBinarizepushButton.setGeometry(QtCore.QRect(667, 190, 121, 23))
        self.thresholdBinarizepushButton.setObjectName("thresholdBinarizepushButton")
        self.convolutePushButton = QtWidgets.QPushButton(self.centralwidget)
        self.convolutePushButton.setGeometry(QtCore.QRect(667, 220, 120, 23))
        self.convolutePushButton.setObjectName("convolutePushButton")
        self.kuwaharaPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.kuwaharaPushButton.setGeometry(QtCore.QRect(665, 250, 121, 23))
        self.kuwaharaPushButton.setObjectName("kuwaharaPushButton")
        self.medianFilterPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.medianFilterPushButton.setGeometry(QtCore.QRect(663, 280, 121, 23))
        self.medianFilterPushButton.setObjectName("medianFilterPushButton")
        self.imageOpsPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.imageOpsPushButton.setGeometry(QtCore.QRect(660, 340, 121, 23))
        self.imageOpsPushButton.setObjectName("imageOpsPushButton")
        self.grayScalePushButton = QtWidgets.QPushButton(self.centralwidget)
        self.grayScalePushButton.setGeometry(QtCore.QRect(660, 370, 121, 23))
        self.grayScalePushButton.setObjectName("grayScalePushButton")
        self.customConvKernelPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.customConvKernelPushButton.setGeometry(QtCore.QRect(660, 400, 121, 23))
        self.customConvKernelPushButton.setObjectName("customConvKernelPushButton")
        self.bpbPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.bpbPushButton.setGeometry(QtCore.QRect(660, 430, 131, 31))
        self.bpbPushButton.setObjectName("bpbPushButton")
        self.morphOpsPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.morphOpsPushButton.setGeometry(QtCore.QRect(660, 470, 131, 23))
        self.morphOpsPushButton.setObjectName("morphOpsPushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionLoad = QtWidgets.QAction(MainWindow)
        self.actionLoad.setObjectName("actionLoad")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.menuFile.addAction(self.actionLoad)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Image Editor"))
        self.imgXKey.setText(_translate("MainWindow", "X:"))
        self.imgYKey.setText(_translate("MainWindow", "Y:"))
        self.imgRKey.setText(_translate("MainWindow", "R:"))
        self.imgGKey.setText(_translate("MainWindow", "G:"))
        self.imgBKey.setText(_translate("MainWindow", "B:"))
        self.histogramPushButton.setText(_translate("MainWindow", "Histogram"))
        self.equalizerPushButton.setText(_translate("MainWindow", "Equalizer"))
        self.brightenPushButton.setText(_translate("MainWindow", "Brightness"))
        self.normalizePushButton.setText(_translate("MainWindow", "Normalize"))
        self.otsuBinarizePushButton.setText(_translate("MainWindow", "Otsu Binarization"))
        self.niblackBinarizepushButton.setText(_translate("MainWindow", "Niblack Binarization"))
        self.thresholdBinarizepushButton.setText(_translate("MainWindow", "Threshold Binarization"))
        self.convolutePushButton.setText(_translate("MainWindow", "Convolution Filter"))
        self.kuwaharaPushButton.setText(_translate("MainWindow", "Kuwahara Filter"))
        self.medianFilterPushButton.setText(_translate("MainWindow", "Median Filter"))
        self.imageOpsPushButton.setText(_translate("MainWindow", "Image Operations"))
        self.grayScalePushButton.setText(_translate("MainWindow", "GrayScale"))
        self.customConvKernelPushButton.setText(_translate("MainWindow", "Custom Conv Kernel"))
        self.bpbPushButton.setText(_translate("MainWindow", "Black percent Binarization"))
        self.morphOpsPushButton.setText(_translate("MainWindow", "Morphological Ops"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.actionLoad.setText(_translate("MainWindow", "Load"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
