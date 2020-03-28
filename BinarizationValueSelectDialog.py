# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BinarizationValueSelectDialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_BinarizationValueSelectDialog(object):
    def setupUi(self, BinarizationValueSelectDialog):
        BinarizationValueSelectDialog.setObjectName("BinarizationValueSelectDialog")
        BinarizationValueSelectDialog.resize(266, 176)
        self.buttonBox = QtWidgets.QDialogButtonBox(BinarizationValueSelectDialog)
        self.buttonBox.setGeometry(QtCore.QRect(20, 130, 221, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.spinBox = QtWidgets.QSpinBox(BinarizationValueSelectDialog)
        self.spinBox.setGeometry(QtCore.QRect(150, 40, 81, 22))
        self.spinBox.setMaximum(255)
        self.spinBox.setObjectName("spinBox")
        self.label = QtWidgets.QLabel(BinarizationValueSelectDialog)
        self.label.setGeometry(QtCore.QRect(20, 43, 71, 16))
        self.label.setObjectName("label")
        self.label_4 = QtWidgets.QLabel(BinarizationValueSelectDialog)
        self.label_4.setGeometry(QtCore.QRect(13, 83, 241, 31))
        self.label_4.setObjectName("label_4")

        self.retranslateUi(BinarizationValueSelectDialog)
        self.buttonBox.accepted.connect(BinarizationValueSelectDialog.accept)
        self.buttonBox.rejected.connect(BinarizationValueSelectDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(BinarizationValueSelectDialog)

    def retranslateUi(self, BinarizationValueSelectDialog):
        _translate = QtCore.QCoreApplication.translate
        BinarizationValueSelectDialog.setWindowTitle(_translate("BinarizationValueSelectDialog", "Dialog"))
        self.label.setText(_translate("BinarizationValueSelectDialog", "Threshold"))
        self.label_4.setText(_translate("BinarizationValueSelectDialog", "WARNING: This will convert image into grayscale"))
