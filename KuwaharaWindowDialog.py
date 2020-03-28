# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'KuwaharaWindowDialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_KuwaharaWindowDialog(object):
    def setupUi(self, KuwaharaWindowDialog):
        KuwaharaWindowDialog.setObjectName("KuwaharaWindowDialog")
        KuwaharaWindowDialog.resize(266, 170)
        self.buttonBox = QtWidgets.QDialogButtonBox(KuwaharaWindowDialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 100, 191, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(KuwaharaWindowDialog)
        self.label.setGeometry(QtCore.QRect(10, 20, 91, 16))
        self.label.setObjectName("label")
        self.spinBox = QtWidgets.QSpinBox(KuwaharaWindowDialog)
        self.spinBox.setGeometry(QtCore.QRect(120, 20, 51, 22))
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(999)
        self.spinBox.setProperty("value", 1)
        self.spinBox.setObjectName("spinBox")
        self.label_2 = QtWidgets.QLabel(KuwaharaWindowDialog)
        self.label_2.setGeometry(QtCore.QRect(20, 60, 47, 13))
        self.label_2.setObjectName("label_2")
        self.valueLabel = QtWidgets.QLabel(KuwaharaWindowDialog)
        self.valueLabel.setGeometry(QtCore.QRect(90, 60, 47, 13))
        self.valueLabel.setObjectName("valueLabel")

        self.retranslateUi(KuwaharaWindowDialog)
        self.buttonBox.accepted.connect(KuwaharaWindowDialog.accept)
        self.buttonBox.rejected.connect(KuwaharaWindowDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(KuwaharaWindowDialog)

    def retranslateUi(self, KuwaharaWindowDialog):
        _translate = QtCore.QCoreApplication.translate
        KuwaharaWindowDialog.setWindowTitle(_translate("KuwaharaWindowDialog", "Dialog"))
        self.label.setText(_translate("KuwaharaWindowDialog", "Window\'s \"n\" Value"))
        self.label_2.setText(_translate("KuwaharaWindowDialog", "4*k+1 ="))
        self.valueLabel.setText(_translate("KuwaharaWindowDialog", "TextLabel"))
