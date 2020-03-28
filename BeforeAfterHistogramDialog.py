# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BeforeAfterHistogramDialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_BeforeAfterHistogramDialog(object):
    def setupUi(self, BeforeAfterHistogramDialog):
        BeforeAfterHistogramDialog.setObjectName("BeforeAfterHistogramDialog")
        BeforeAfterHistogramDialog.resize(924, 605)
        self.beforeHistogramWidget = HistogramWidget(BeforeAfterHistogramDialog)
        self.beforeHistogramWidget.setGeometry(QtCore.QRect(10, 30, 581, 261))
        self.beforeHistogramWidget.setObjectName("beforeHistogramWidget")
        self.buttonBox = QtWidgets.QDialogButtonBox(BeforeAfterHistogramDialog)
        self.buttonBox.setGeometry(QtCore.QRect(750, 570, 156, 23))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(BeforeAfterHistogramDialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(BeforeAfterHistogramDialog)
        self.label_2.setGeometry(QtCore.QRect(10, 300, 47, 13))
        self.label_2.setObjectName("label_2")
        self.afterHistogramWidget = HistogramWidget(BeforeAfterHistogramDialog)
        self.afterHistogramWidget.setGeometry(QtCore.QRect(10, 320, 581, 241))
        self.afterHistogramWidget.setObjectName("afterHistogramWidget")
        self.beforeImageLabel = QtWidgets.QLabel(BeforeAfterHistogramDialog)
        self.beforeImageLabel.setGeometry(QtCore.QRect(600, 30, 301, 261))
        self.beforeImageLabel.setObjectName("beforeImageLabel")
        self.afterImageLabel = QtWidgets.QLabel(BeforeAfterHistogramDialog)
        self.afterImageLabel.setGeometry(QtCore.QRect(600, 320, 301, 241))
        self.afterImageLabel.setObjectName("afterImageLabel")

        self.retranslateUi(BeforeAfterHistogramDialog)
        QtCore.QMetaObject.connectSlotsByName(BeforeAfterHistogramDialog)

    def retranslateUi(self, BeforeAfterHistogramDialog):
        _translate = QtCore.QCoreApplication.translate
        BeforeAfterHistogramDialog.setWindowTitle(_translate("BeforeAfterHistogramDialog", "Dialog"))
        self.label.setText(_translate("BeforeAfterHistogramDialog", "Before"))
        self.label_2.setText(_translate("BeforeAfterHistogramDialog", "After"))
        self.beforeImageLabel.setText(_translate("BeforeAfterHistogramDialog", "TextLabel"))
        self.afterImageLabel.setText(_translate("BeforeAfterHistogramDialog", "TextLabel"))
from HistogramWidget import HistogramWidget
