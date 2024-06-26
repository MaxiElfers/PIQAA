# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\workspace\python_in_qgis_arcgis\PIQAA\exercise_8\muenster_city_district_tool\getDataDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_get(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.InputField = QtWidgets.QGroupBox(Dialog)
        self.InputField.setGeometry(QtCore.QRect(20, 20, 351, 231))
        self.InputField.setObjectName("InputField")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(120, 260, 151, 32))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.InputField)
        self.label.setGeometry(QtCore.QRect(25, 25, 491, 150))
        self.label.setWordWrap(True)
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # Add close functionality to the OK button
        self.pushButton.clicked.connect(Dialog.close)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Data Dialog"))
        self.InputField.setTitle(_translate("Dialog", "Selected Feature Information"))
        self.pushButton.setText(_translate("Dialog", "OK"))

    # Fill the input field with the information array
    def fillInputField(self, information_array):
        self.label.setText("Name: " + str(information_array[0]) + "\n" + 
                           "P_District: " + str(information_array[1]) + "\n" + 
                           "Area: " + str(information_array[2]) + "\n" + 
                           "Households: " + str(information_array[3]) + "\n" + 
                           "Parcels: "+ str(information_array[4]) + "\n" + 
                           "Schools: " + str(information_array[5][0]) + "\n" +
                           "Pools: " + str(information_array[6][0]))
