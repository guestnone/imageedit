# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BlackBinarizationDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_BlackBinarizationValueDialog(object):
    def setupUi(self, BlackBinarizationValueDialog):
        BlackBinarizationValueDialog.setObjectName("BlackBinarizationValueDialog")
        BlackBinarizationValueDialog.resize(400, 189)
        self.buttonBox = QtWidgets.QDialogButtonBox(BlackBinarizationValueDialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 130, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalSlider = QtWidgets.QSlider(BlackBinarizationValueDialog)
        self.horizontalSlider.setGeometry(QtCore.QRect(10, 50, 341, 22))
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setSingleStep(10)
        self.horizontalSlider.setPageStep(10)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.label = QtWidgets.QLabel(BlackBinarizationValueDialog)
        self.label.setGeometry(QtCore.QRect(10, 20, 91, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(BlackBinarizationValueDialog)
        self.label_2.setGeometry(QtCore.QRect(10, 80, 47, 13))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(BlackBinarizationValueDialog)
        self.label_3.setGeometry(QtCore.QRect(170, 80, 47, 13))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(BlackBinarizationValueDialog)
        self.label_4.setGeometry(QtCore.QRect(330, 80, 47, 13))
        self.label_4.setObjectName("label_4")

        self.retranslateUi(BlackBinarizationValueDialog)
        self.buttonBox.accepted.connect(BlackBinarizationValueDialog.accept)
        self.buttonBox.rejected.connect(BlackBinarizationValueDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(BlackBinarizationValueDialog)

    def retranslateUi(self, BlackBinarizationValueDialog):
        _translate = QtCore.QCoreApplication.translate
        BlackBinarizationValueDialog.setWindowTitle(_translate("BlackBinarizationValueDialog", "Percent Of Black binarization settings"))
        self.label.setText(_translate("BlackBinarizationValueDialog", "Percent of black"))
        self.label_2.setText(_translate("BlackBinarizationValueDialog", "0%"))
        self.label_3.setText(_translate("BlackBinarizationValueDialog", "50%"))
        self.label_4.setText(_translate("BlackBinarizationValueDialog", "100%"))
