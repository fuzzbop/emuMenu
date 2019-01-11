# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'assets/addConsoleDialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_add_console_dialog(object):
    def setupUi(self, add_console_dialog):
        add_console_dialog.setObjectName("add_console_dialog")
        add_console_dialog.resize(728, 164)
        self.gridLayout = QtWidgets.QGridLayout(add_console_dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.console_add_button_box = QtWidgets.QDialogButtonBox(add_console_dialog)
        self.console_add_button_box.setOrientation(QtCore.Qt.Horizontal)
        self.console_add_button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.console_add_button_box.setObjectName("console_add_button_box")
        self.gridLayout.addWidget(self.console_add_button_box, 2, 0, 1, 1)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setSpacing(5)
        self.main_layout.setObjectName("main_layout")
        self.name_layout = QtWidgets.QHBoxLayout()
        self.name_layout.setSpacing(10)
        self.name_layout.setObjectName("name_layout")
        self.console_name_label = QtWidgets.QLabel(add_console_dialog)
        self.console_name_label.setMinimumSize(QtCore.QSize(150, 35))
        self.console_name_label.setMaximumSize(QtCore.QSize(150, 35))
        self.console_name_label.setFrameShape(QtWidgets.QFrame.Panel)
        self.console_name_label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.console_name_label.setObjectName("console_name_label")
        self.name_layout.addWidget(self.console_name_label)
        self.console_name_text = QtWidgets.QLineEdit(add_console_dialog)
        self.console_name_text.setObjectName("console_name_text")
        self.name_layout.addWidget(self.console_name_text)
        self.main_layout.addLayout(self.name_layout)
        self.command_layout = QtWidgets.QHBoxLayout()
        self.command_layout.setSpacing(10)
        self.command_layout.setObjectName("command_layout")
        self.command_label = QtWidgets.QLabel(add_console_dialog)
        self.command_label.setMinimumSize(QtCore.QSize(150, 35))
        self.command_label.setMaximumSize(QtCore.QSize(150, 35))
        self.command_label.setFrameShape(QtWidgets.QFrame.Panel)
        self.command_label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.command_label.setObjectName("command_label")
        self.command_layout.addWidget(self.command_label)
        self.command_text = QtWidgets.QLineEdit(add_console_dialog)
        self.command_text.setObjectName("command_text")
        self.command_layout.addWidget(self.command_text)
        self.main_layout.addLayout(self.command_layout)
        self.gridLayout.addLayout(self.main_layout, 1, 0, 1, 1)
        self.Description_label = QtWidgets.QLabel(add_console_dialog)
        self.Description_label.setAlignment(QtCore.Qt.AlignCenter)
        self.Description_label.setObjectName("Description_label")
        self.gridLayout.addWidget(self.Description_label, 0, 0, 1, 1)

        self.retranslateUi(add_console_dialog)
        self.console_add_button_box.accepted.connect(add_console_dialog.accept)
        self.console_add_button_box.rejected.connect(add_console_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(add_console_dialog)

    def retranslateUi(self, add_console_dialog):
        _translate = QtCore.QCoreApplication.translate
        add_console_dialog.setWindowTitle(_translate("add_console_dialog", "Add New Console"))
        self.console_name_label.setText(_translate("add_console_dialog", "Console Name:"))
        self.command_label.setText(_translate("add_console_dialog", "Command :"))
        self.Description_label.setText(_translate("add_console_dialog", "Add a console to emuMenu.Use <ROM> or <BASENAME> in command to replace rom"))

