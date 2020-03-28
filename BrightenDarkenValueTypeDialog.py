# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BrightenDarkenValueTypeDialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_BrightenDarkenValueTypeDialog(object):
    def setupUi(self, BrightenDarkenValueTypeDialog):
        BrightenDarkenValueTypeDialog.setObjectName("BrightenDarkenValueTypeDialog")
        BrightenDarkenValueTypeDialog.resize(241, 154)
        self.buttonBox = QtWidgets.QDialogButtonBox(BrightenDarkenValueTypeDialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 100, 171, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.minDoubleSpinBoxPhi = QtWidgets.QDoubleSpinBox(BrightenDarkenValueTypeDialog)
        self.minDoubleSpinBoxPhi.setGeometry(QtCore.QRect(100, 20, 81, 22))
        self.minDoubleSpinBoxPhi.setObjectName("minDoubleSpinBoxPhi")
        self.label = QtWidgets.QLabel(BrightenDarkenValueTypeDialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 47, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(BrightenDarkenValueTypeDialog)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 47, 21))
        self.label_2.setObjectName("label_2")
        self.minDoubleSpinBoxTheta = QtWidgets.QDoubleSpinBox(BrightenDarkenValueTypeDialog)
        self.minDoubleSpinBoxTheta.setGeometry(QtCore.QRect(100, 70, 81, 22))
        self.minDoubleSpinBoxTheta.setObjectName("minDoubleSpinBoxTheta")

        self.retranslateUi(BrightenDarkenValueTypeDialog)
        self.buttonBox.accepted.connect(BrightenDarkenValueTypeDialog.accept)
        self.buttonBox.rejected.connect(BrightenDarkenValueTypeDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(BrightenDarkenValueTypeDialog)

    def retranslateUi(self, BrightenDarkenValueTypeDialog):
        _translate = QtCore.QCoreApplication.translate
        BrightenDarkenValueTypeDialog.setWindowTitle(_translate("BrightenDarkenValueTypeDialog", "Dialog"))
        self.label.setText(_translate("BrightenDarkenValueTypeDialog", "Phi"))
        self.label_2.setText(_translate("BrightenDarkenValueTypeDialog", "Theta"))
