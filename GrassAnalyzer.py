import json
from typing import List, NamedTuple

import cv2
import numpy as np
import qimage2ndarray
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QWidget, QFileDialog, QDialogButtonBox, QGraphicsScene

from PostAnalyzeDialogBase import Ui_PostAnalyzeDialogBase
from PreAnalyzeDialogBase import Ui_PreAnalyzeDialogBase


class Color(NamedTuple):
    Hue: int
    Saturation: int
    Value: int

class ColorLimits(NamedTuple):
    Begin: Color
    End: Color


class ColorDetectVariable:
    Limits: List[ColorLimits]


class Results:
    DetectVar: ColorDetectVariable

    InputImage: np.ndarray
    PostSeamsImage: np.ndarray
    PostClosingImage: np.ndarray
    PostFillingImage: np.ndarray

    PercentPostSeams: float
    PercentPostClosing: float
    PercentFinal: float


def getDefaultSettings():
    vars = ColorDetectVariable()
    vars.Limits = []

    from1 = (40, 0, 0)
    to1 = (60, 255, 255)
    vars.Limits.append(ColorLimits(from1, to1))

    from2 = (190, 0, 0)
    to2 = (230, 255, 255)
    vars.Limits.append(ColorLimits(from2, to2))

    return vars


def loadFromJsonFile(path="./grassVars.json"):
    fileToOpen = open(path, "r")
    file = json.load(fp=fileToOpen)
    return file


def saveDefaults(path="./grassVars.json"):
    fileToSave = open(path, 'w')
    json.dump(getDefaultSettings(), fp=fileToSave, indent=4)
    fileToSave.close()


def Analyze(image: QImage, vars: ColorDetectVariable) -> (Results, bool):
    results = Results
    results.InputImage = qimage2ndarray.rgb_view(image, 'little')
    tmpHsv = cv2.cvtColor(results.InputImage, cv2.COLOR_BGR2HSV)

    mask = None
    for (limit) in vars.Limits:
        if mask is None:
            mask = cv2.inRange(tmpHsv, limit.Begin, limit.End)
        else:
            mask = mask + cv2.inRange(tmpHsv, limit.Begin, limit.End)

    results.PostSeamsImage = cv2.bitwise_and(results.InputImage, results.InputImage, mask=mask)

    return results, True


class PreAnalyzeGui(QDialog):
    def __init__(self):
        QWidget.__init__(self)
        self.path = ""
        self.isChange = False
        self.ui = Ui_PreAnalyzeDialogBase()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.handleOK)
        self.ui.buttonBox.rejected.connect(self.handleCancel)
        self.ui.plainTextEdit.setPlainText(self.path)
        self.ui.locPushButton.clicked.connect(self.handleGetPath)

    @pyqtSlot()
    def handleOK(self):
        self.isChange = True

    @pyqtSlot()
    def handleCancel(self):
        self.isChange = False

    @pyqtSlot()
    def handleGetPath(self):
        name, selFilter = QFileDialog.getOpenFileName(self, 'Open Settings', "",
                                                      "Settings File (*.json);;All Files (*)", )
        if name:
            self.path = name
            self.ui.plainTextEdit.setPlainText(self.path)

    def getDoIt(self):
        return self.isChange

    def getPath(self):
        return self.path

    def getIsUseDefault(self):
        return self.ui.checkBox.isChecked()


class PostAnalyzeGui(QDialog):
    def __init__(self, results: Results):
        QWidget.__init__(self)
        self.results = results
        self.ui = Ui_PostAnalyzeDialogBase()
        self.ui.setupUi(self)
        self.ui.buttonBox.button(QDialogButtonBox.Save).clicked.connect(self.doSave)

        #Input Image
        inputScene = QGraphicsScene()
        inputPixmap = QPixmap.fromImage(qimage2ndarray.array2qimage(results.InputImage))
        inputScene.addPixmap(inputPixmap)
        self.ui.inputGraphicsView.setScene(inputScene)

        # PostSeams
        postSeamsScene = QGraphicsScene()
        postSeamsPixmap = QPixmap.fromImage(qimage2ndarray.array2qimage(results.PostSeamsImage))
        postSeamsScene.addPixmap(postSeamsPixmap)
        self.ui.postFilterGraphicsView.setScene(postSeamsScene)

    @pyqtSlot()
    def doSave(self):
        name = QFileDialog.getExistingDirectory(self, "Save Results")
        if name:
            print("saving")


class GrassAnalyzerMain:
    def __init__(self, image):
        self.dialog = PreAnalyzeGui()
        self.dialog.setModal(True)
        self.dialog.exec_()
        if self.dialog.getDoIt():
            print("GOWNO")
            if self.dialog.getIsUseDefault():
                self.vars = getDefaultSettings()
            else:
                self.vars = loadFromJsonFile(self.dialog.getPath())

            results, ok = Analyze(image, self.vars)
            if ok:
                self.dialog = PostAnalyzeGui(results)
                self.dialog.setModal(True)
                self.dialog.exec_()
