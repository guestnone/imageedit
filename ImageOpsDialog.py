# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ImageOpsDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_imageOpsDialog(object):
    def setupUi(self, imageOpsDialog):
        imageOpsDialog.setObjectName("imageOpsDialog")
        imageOpsDialog.resize(400, 152)
        imageOpsDialog.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(imageOpsDialog)
        self.buttonBox.setGeometry(QtCore.QRect(40, 100, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(imageOpsDialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(20, 10, 361, 81))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(6, 5, 11, 0)
        self.formLayout.setHorizontalSpacing(7)
        self.formLayout.setVerticalSpacing(16)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.valueSpinBox = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.valueSpinBox.setMinimum(-255)
        self.valueSpinBox.setMaximum(255)
        self.valueSpinBox.setObjectName("valueSpinBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.valueSpinBox)
        self.comboBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comboBox)

        self.retranslateUi(imageOpsDialog)
        self.buttonBox.accepted.connect(imageOpsDialog.accept)
        self.buttonBox.rejected.connect(imageOpsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(imageOpsDialog)

    def retranslateUi(self, imageOpsDialog):
        _translate = QtCore.QCoreApplication.translate
        imageOpsDialog.setWindowTitle(_translate("imageOpsDialog", "Image Opertations Select"))
        self.label.setText(_translate("imageOpsDialog", "Type"))
        self.label_2.setText(_translate("imageOpsDialog", "Value"))
        self.comboBox.setItemText(0, _translate("imageOpsDialog", "Add"))
        self.comboBox.setItemText(1, _translate("imageOpsDialog", "Subtract"))
        self.comboBox.setItemText(2, _translate("imageOpsDialog", "Multiply"))
        self.comboBox.setItemText(3, _translate("imageOpsDialog", "Divide"))
        self.comboBox.setItemText(4, _translate("imageOpsDialog", "Brighten"))
        self.comboBox.setItemText(5, _translate("imageOpsDialog", "Darken"))