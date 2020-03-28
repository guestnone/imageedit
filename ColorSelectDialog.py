# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ColorSelectDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ColorSelectDialog(object):
    def setupUi(self, ColorSelectDialog):
        ColorSelectDialog.setObjectName("ColorSelectDialog")
        ColorSelectDialog.resize(282, 204)
        self.buttonBox = QtWidgets.QDialogButtonBox(ColorSelectDialog)
        self.buttonBox.setGeometry(QtCore.QRect(110, 150, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(ColorSelectDialog)
        self.label.setGeometry(QtCore.QRect(20, 18, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(ColorSelectDialog)
        self.label_2.setGeometry(QtCore.QRect(20, 58, 47, 13))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(ColorSelectDialog)
        self.label_3.setGeometry(QtCore.QRect(20, 100, 47, 13))
        self.label_3.setObjectName("label_3")
        self.redSpinBox = QtWidgets.QSpinBox(ColorSelectDialog)
        self.redSpinBox.setGeometry(QtCore.QRect(220, 13, 42, 22))
        self.redSpinBox.setMaximum(255)
        self.redSpinBox.setObjectName("redSpinBox")
        self.greenSpinBox = QtWidgets.QSpinBox(ColorSelectDialog)
        self.greenSpinBox.setGeometry(QtCore.QRect(220, 54, 42, 22))
        self.greenSpinBox.setMaximum(255)
        self.greenSpinBox.setObjectName("greenSpinBox")
        self.blueSpinBox = QtWidgets.QSpinBox(ColorSelectDialog)
        self.blueSpinBox.setGeometry(QtCore.QRect(220, 96, 42, 22))
        self.blueSpinBox.setMaximum(255)
        self.blueSpinBox.setObjectName("blueSpinBox")
        self.colorSelectorPushButton = QtWidgets.QPushButton(ColorSelectDialog)
        self.colorSelectorPushButton.setGeometry(QtCore.QRect(30, 156, 75, 21))
        self.colorSelectorPushButton.setObjectName("colorSelectorPushButton")

        self.retranslateUi(ColorSelectDialog)
        self.buttonBox.accepted.connect(ColorSelectDialog.accept)
        self.buttonBox.rejected.connect(ColorSelectDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ColorSelectDialog)

    def retranslateUi(self, ColorSelectDialog):
        _translate = QtCore.QCoreApplication.translate
        ColorSelectDialog.setWindowTitle(_translate("ColorSelectDialog", "Change Color"))
        self.label.setText(_translate("ColorSelectDialog", "Red:"))
        self.label_2.setText(_translate("ColorSelectDialog", "Green:"))
        self.label_3.setText(_translate("ColorSelectDialog", "Blue:"))
        self.colorSelectorPushButton.setText(_translate("ColorSelectDialog", "Select Color"))
