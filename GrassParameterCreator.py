import qimage2ndarray
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QWidget, QGraphicsScene, QDialogButtonBox, QFileDialog
from PyQt5.QtCore import Qt, QAbstractTableModel, pyqtSlot
import pandas as pd
from typing import List

from GrassAnalyzer import ColorLimits, Color, GetSeamsImage, ColorDetectVariable, saveToFile
from GrassParameterCreatorDialog import Ui_GrassParameterCreatorDialog


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])


class GrassParameterCreatorDialogImpl(QDialog):
    def __init__(self, image):
        QWidget.__init__(self)
        self.isChange = False
        self.ui = Ui_GrassParameterCreatorDialog()
        self.ui.setupUi(self)

        self.image = image
        inputScene = QGraphicsScene()
        inputScene.addPixmap(QPixmap.fromImage(self.image))
        self.ui.graphicsView.setScene(inputScene)
        self.data = pd.DataFrame([
        ], columns=['Begin H', 'Begin S', 'Begin V', 'End H', 'End S', 'End V'])
        self.model = TableModel(self.data)
        self.ui.tableView.setModel(self.model)
        self.ui.currCreatedLimitsPushButton.clicked.connect(self.generateForNew)
        self.ui.allLimitsPushButton.clicked.connect(self.generateForAll)
        self.ui.addPushButton.clicked.connect(self.add)
        self.ui.buttonBox.button(QDialogButtonBox.Save).clicked.connect(self.doSave)

    @pyqtSlot()
    def generateForNew(self):
        begin = Color(self.ui.hBeginSpinBox.value(), self.ui.sBeginSpinBox.value(), self.ui.vBeginSpinBox.value())
        end = Color(self.ui.hEndSpinBox.value(), self.ui.sEndSpinBox.value(), self.ui.vEndSpinBox.value())
        theInput = [ColorLimits(begin, end)]
        out = GetSeamsImage(qimage2ndarray.rgb_view(self.image, 'little'), theInput)

        scene = QGraphicsScene()
        scene.addPixmap(QPixmap.fromImage(qimage2ndarray.array2qimage(out)))
        self.ui.graphicsView.setScene(scene)


    @pyqtSlot()
    def generateForAll(self):
        theInput = []
        for index, limitSet in self.data.iterrows():
            begin = Color(limitSet['Begin H'], limitSet['Begin S'], limitSet['Begin V'])
            end = Color(limitSet['End H'], limitSet['End S'], limitSet['End V'])
            theInput.append(ColorLimits(begin, end))

        out = GetSeamsImage(qimage2ndarray.rgb_view(self.image, 'little'), theInput)

        scene = QGraphicsScene()
        scene.addPixmap(QPixmap.fromImage(qimage2ndarray.array2qimage(out)))
        self.ui.graphicsView.setScene(scene)

    @pyqtSlot()
    def add(self):
        newData = pd.DataFrame([
            [self.ui.hBeginSpinBox.value(), self.ui.sBeginSpinBox.value(), self.ui.vBeginSpinBox.value(),
             self.ui.hEndSpinBox.value(), self.ui.sEndSpinBox.value(), self.ui.vEndSpinBox.value()]
        ], columns=['Begin H', 'Begin S', 'Begin V', 'End H', 'End S', 'End V'])
        self.data = pd.concat([self.data, newData])
        self.model = TableModel(self.data)
        self.ui.tableView.setModel(self.model)

    @pyqtSlot()
    def doSave(self):
        name, selFilter = QFileDialog.getSaveFileName(self, "Save Settings", "",
                                                      "JSON Settings file (*.json)")

        if name:
            theInput = []
            for index, limitSet in self.data.iterrows():
                begin = Color(limitSet['Begin H'], limitSet['Begin S'], limitSet['Begin V'])
                end = Color(limitSet['End H'], limitSet['End S'], limitSet['End V'])
                theInput.append(ColorLimits(begin, end))
            saveToFile(theInput, name)




class GrassParameterCreatorMain:
    def __init__(self, image):
        self.dialog = GrassParameterCreatorDialogImpl(image)
        self.dialog.setModal(True)
        self.dialog.exec_()
