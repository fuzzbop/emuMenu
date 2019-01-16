# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'assets/customRomDialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_launch_rom_dialog(object):
    def setupUi(self, launch_rom_dialog):
        launch_rom_dialog.setObjectName("launch_rom_dialog")
        launch_rom_dialog.resize(654, 91)
        self.gridLayout = QtWidgets.QGridLayout(launch_rom_dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.launch_rom_buttonbox = QtWidgets.QDialogButtonBox(launch_rom_dialog)
        self.launch_rom_buttonbox.setOrientation(QtCore.Qt.Horizontal)
        self.launch_rom_buttonbox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.launch_rom_buttonbox.setObjectName("launch_rom_buttonbox")
        self.gridLayout.addWidget(self.launch_rom_buttonbox, 1, 0, 1, 1)
        self.launch_rom_dialog_2 = QtWidgets.QHBoxLayout()
        self.launch_rom_dialog_2.setObjectName("launch_rom_dialog_2")
        self.rom_location_label = QtWidgets.QLabel(launch_rom_dialog)
        self.rom_location_label.setFrameShape(QtWidgets.QFrame.Panel)
        self.rom_location_label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.rom_location_label.setObjectName("rom_location_label")
        self.launch_rom_dialog_2.addWidget(self.rom_location_label)
        self.rom_location_line_edit = QtWidgets.QLineEdit(launch_rom_dialog)
        self.rom_location_line_edit.setObjectName("rom_location_line_edit")
        self.launch_rom_dialog_2.addWidget(self.rom_location_line_edit)
        self.rom_location_button = QtWidgets.QPushButton(launch_rom_dialog)
        self.rom_location_button.setObjectName("rom_location_button")
        self.launch_rom_dialog_2.addWidget(self.rom_location_button)
        self.gridLayout.addLayout(self.launch_rom_dialog_2, 0, 0, 1, 1)

        self.retranslateUi(launch_rom_dialog)
        self.launch_rom_buttonbox.accepted.connect(launch_rom_dialog.accept)
        self.launch_rom_buttonbox.rejected.connect(launch_rom_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(launch_rom_dialog)

    def retranslateUi(self, launch_rom_dialog):
        _translate = QtCore.QCoreApplication.translate
        launch_rom_dialog.setWindowTitle(_translate("launch_rom_dialog", "Launch Unlisted Rom"))
        self.rom_location_label.setText(_translate("launch_rom_dialog", "Rom Location"))
        self.rom_location_button.setText(_translate("launch_rom_dialog", "Open"))

