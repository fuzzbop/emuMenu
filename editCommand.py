# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'assets/editCommand.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_edit_command_dialog(object):
    def setupUi(self, edit_command_dialog):
        edit_command_dialog.setObjectName("edit_command_dialog")
        edit_command_dialog.resize(509, 159)
        self.gridLayout = QtWidgets.QGridLayout(edit_command_dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.console_layout = QtWidgets.QHBoxLayout()
        self.console_layout.setSpacing(10)
        self.console_layout.setObjectName("console_layout")
        self.console_name_label = QtWidgets.QLabel(edit_command_dialog)
        self.console_name_label.setMinimumSize(QtCore.QSize(150, 35))
        self.console_name_label.setMaximumSize(QtCore.QSize(150, 35))
        self.console_name_label.setFrameShape(QtWidgets.QFrame.Panel)
        self.console_name_label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.console_name_label.setObjectName("console_name_label")
        self.console_layout.addWidget(self.console_name_label)
        self.console_name_combo = QtWidgets.QComboBox(edit_command_dialog)
        self.console_name_combo.setMinimumSize(QtCore.QSize(0, 35))
        self.console_name_combo.setMaximumSize(QtCore.QSize(16777215, 35))
        self.console_name_combo.setObjectName("console_name_combo")
        self.console_layout.addWidget(self.console_name_combo)
        self.gridLayout.addLayout(self.console_layout, 0, 0, 1, 1)
        self.edit_command_label = QtWidgets.QLabel(edit_command_dialog)
        self.edit_command_label.setFrameShape(QtWidgets.QFrame.Panel)
        self.edit_command_label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.edit_command_label.setAlignment(QtCore.Qt.AlignCenter)
        self.edit_command_label.setObjectName("edit_command_label")
        self.gridLayout.addWidget(self.edit_command_label, 1, 0, 1, 1)
        self.edit_command_line_edit = QtWidgets.QLineEdit(edit_command_dialog)
        self.edit_command_line_edit.setObjectName("edit_command_line_edit")
        self.gridLayout.addWidget(self.edit_command_line_edit, 2, 0, 1, 1)
        self.edit_command_button_box = QtWidgets.QDialogButtonBox(edit_command_dialog)
        self.edit_command_button_box.setOrientation(QtCore.Qt.Horizontal)
        self.edit_command_button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.edit_command_button_box.setObjectName("edit_command_button_box")
        self.gridLayout.addWidget(self.edit_command_button_box, 3, 0, 1, 1)

        self.retranslateUi(edit_command_dialog)
        self.edit_command_button_box.accepted.connect(edit_command_dialog.accept)
        self.edit_command_button_box.rejected.connect(edit_command_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(edit_command_dialog)

    def retranslateUi(self, edit_command_dialog):
        _translate = QtCore.QCoreApplication.translate
        edit_command_dialog.setWindowTitle(_translate("edit_command_dialog", "Edit Command"))
        self.console_name_label.setText(_translate("edit_command_dialog", "Console Name: "))
        self.edit_command_label.setText(_translate("edit_command_dialog", "Edit command below"))

