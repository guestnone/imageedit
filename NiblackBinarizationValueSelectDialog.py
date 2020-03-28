# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NiblackBinarizationValueSelectDialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NiblackBinarizationValueSelectDialog(object):
    def setupUi(self, NiblackBinarizationValueSelectDialog):
        NiblackBinarizationValueSelectDialog.setObjectName("NiblackBinarizationValueSelectDialog")
        NiblackBinarizationValueSelectDialog.resize(266, 207)
        self.buttonBox = QtWidgets.QDialogButtonBox(NiblackBinarizationValueSelectDialog)
        self.buttonBox.setGeometry(QtCore.QRect(20, 160, 221, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.localThresholdDoubleSpinBox = QtWidgets.QDoubleSpinBox(NiblackBinarizationValueSelectDialog)
        self.localThresholdDoubleSpinBox.setGeometry(QtCore.QRect(150, 86, 81, 22))
        self.localThresholdDoubleSpinBox.setDecimals(2)
        self.localThresholdDoubleSpinBox.setMinimum(-0.2)
        self.localThresholdDoubleSpinBox.setMaximum(-0.1)
        self.localThresholdDoubleSpinBox.setSingleStep(0.01)
        self.localThresholdDoubleSpinBox.setStepType(QtWidgets.QAbstractSpinBox.DefaultStepType)
        self.localThresholdDoubleSpinBox.setProperty("value", -0.1)
        self.localThresholdDoubleSpinBox.setObjectName("localThresholdDoubleSpinBox")
        self.label = QtWidgets.QLabel(NiblackBinarizationValueSelectDialog)
        self.label.setGeometry(QtCore.QRect(20, 89, 81, 16))
        self.label.setObjectName("label")
        self.localWindowSpinBox = QtWidgets.QSpinBox(NiblackBinarizationValueSelectDialog)
        self.localWindowSpinBox.setGeometry(QtCore.QRect(150, 53, 81, 22))
        self.localWindowSpinBox.setMinimum(1)
        self.localWindowSpinBox.setMaximum(255)
        self.localWindowSpinBox.setSingleStep(2)
        self.localWindowSpinBox.setObjectName("localWindowSpinBox")
        self.label_2 = QtWidgets.QLabel(NiblackBinarizationValueSelectDialog)
        self.label_2.setGeometry(QtCore.QRect(20, 56, 81, 16))
        self.label_2.setObjectName("label_2")
        self.globalThresholdSpinBox = QtWidgets.QSpinBox(NiblackBinarizationValueSelectDialog)
        self.globalThresholdSpinBox.setGeometry(QtCore.QRect(150, 24, 81, 22))
        self.globalThresholdSpinBox.setMaximum(255)
        self.globalThresholdSpinBox.setObjectName("globalThresholdSpinBox")
        self.label_3 = QtWidgets.QLabel(NiblackBinarizationValueSelectDialog)
        self.label_3.setGeometry(QtCore.QRect(20, 27, 81, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(NiblackBinarizationValueSelectDialog)
        self.label_4.setGeometry(QtCore.QRect(10, 120, 241, 31))
        self.label_4.setObjectName("label_4")

        self.retranslateUi(NiblackBinarizationValueSelectDialog)
        self.buttonBox.accepted.connect(NiblackBinarizationValueSelectDialog.accept)
        self.buttonBox.rejected.connect(NiblackBinarizationValueSelectDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NiblackBinarizationValueSelectDialog)

    def retranslateUi(self, NiblackBinarizationValueSelectDialog):
        _translate = QtCore.QCoreApplication.translate
        NiblackBinarizationValueSelectDialog.setWindowTitle(_translate("NiblackBinarizationValueSelectDialog", "Dialog"))
        self.label.setText(_translate("NiblackBinarizationValueSelectDialog", "Local Threshold"))
        self.label_2.setText(_translate("NiblackBinarizationValueSelectDialog", "Local Window"))
        self.label_3.setText(_translate("NiblackBinarizationValueSelectDialog", "Global Threshold"))
        self.label_4.setText(_translate("NiblackBinarizationValueSelectDialog", "WARNING: This will convert image into grayscale"))
