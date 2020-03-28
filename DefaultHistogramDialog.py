# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DefaultHistogramDialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DefaultHistogramDialog(object):
    def setupUi(self, DefaultHistogramDialog):
        DefaultHistogramDialog.setObjectName("DefaultHistogramDialog")
        DefaultHistogramDialog.resize(603, 320)
        self.widget = HistogramWidget(DefaultHistogramDialog)
        self.widget.setGeometry(QtCore.QRect(10, 10, 581, 271))
        self.widget.setObjectName("widget")
        self.pushButton = QtWidgets.QPushButton(DefaultHistogramDialog)
        self.pushButton.setGeometry(QtCore.QRect(510, 290, 75, 23))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(DefaultHistogramDialog)
        QtCore.QMetaObject.connectSlotsByName(DefaultHistogramDialog)

    def retranslateUi(self, DefaultHistogramDialog):
        _translate = QtCore.QCoreApplication.translate
        DefaultHistogramDialog.setWindowTitle(_translate("DefaultHistogramDialog", "Dialog"))
        self.pushButton.setText(_translate("DefaultHistogramDialog", "Close"))
from HistogramWidget import HistogramWidget
