# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MedianSizeDialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MedianSizeDialog(object):
    def setupUi(self, MedianSizeDialog):
        MedianSizeDialog.setObjectName("MedianSizeDialog")
        MedianSizeDialog.resize(253, 169)
        self.buttonBox = QtWidgets.QDialogButtonBox(MedianSizeDialog)
        self.buttonBox.setGeometry(QtCore.QRect(20, 110, 201, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.spinBox = QtWidgets.QSpinBox(MedianSizeDialog)
        self.spinBox.setGeometry(QtCore.QRect(130, 18, 42, 22))
        self.spinBox.setObjectName("spinBox")
        self.label = QtWidgets.QLabel(MedianSizeDialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 47, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(MedianSizeDialog)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 91, 16))
        self.label_2.setObjectName("label_2")
        self.filterSizeLabel = QtWidgets.QLabel(MedianSizeDialog)
        self.filterSizeLabel.setGeometry(QtCore.QRect(110, 73, 47, 13))
        self.filterSizeLabel.setObjectName("filterSizeLabel")

        self.retranslateUi(MedianSizeDialog)
        self.buttonBox.accepted.connect(MedianSizeDialog.accept)
        self.buttonBox.rejected.connect(MedianSizeDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(MedianSizeDialog)

    def retranslateUi(self, MedianSizeDialog):
        _translate = QtCore.QCoreApplication.translate
        MedianSizeDialog.setWindowTitle(_translate("MedianSizeDialog", "Dialog"))
        self.label.setText(_translate("MedianSizeDialog", "Filter Size"))
        self.label_2.setText(_translate("MedianSizeDialog", "Filter Rectangle:"))
        self.filterSizeLabel.setText(_translate("MedianSizeDialog", "TextLabel"))
