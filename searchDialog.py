# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'assets/searchDialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_search_dialog(object):
    def setupUi(self, search_dialog):
        search_dialog.setObjectName("search_dialog")
        search_dialog.resize(783, 636)
        self.gridLayout = QtWidgets.QGridLayout(search_dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.search_dialog_buttonbox = QtWidgets.QDialogButtonBox(search_dialog)
        self.search_dialog_buttonbox.setOrientation(QtCore.Qt.Horizontal)
        self.search_dialog_buttonbox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.search_dialog_buttonbox.setObjectName("search_dialog_buttonbox")
        self.gridLayout.addWidget(self.search_dialog_buttonbox, 2, 0, 1, 1)
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setObjectName("main_layout")
        self.console_layout = QtWidgets.QVBoxLayout()
        self.console_layout.setObjectName("console_layout")
        self.console_label = QtWidgets.QLabel(search_dialog)
        self.console_label.setFrameShape(QtWidgets.QFrame.Panel)
        self.console_label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.console_label.setAlignment(QtCore.Qt.AlignCenter)
        self.console_label.setObjectName("console_label")
        self.console_layout.addWidget(self.console_label)
        self.console_list = QtWidgets.QListWidget(search_dialog)
        self.console_list.setObjectName("console_list")
        self.console_layout.addWidget(self.console_list)
        self.main_layout.addLayout(self.console_layout)
        self.rom_layout = QtWidgets.QVBoxLayout()
        self.rom_layout.setObjectName("rom_layout")
        self.rom_label = QtWidgets.QLabel(search_dialog)
        self.rom_label.setFrameShape(QtWidgets.QFrame.Panel)
        self.rom_label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.rom_label.setAlignment(QtCore.Qt.AlignCenter)
        self.rom_label.setObjectName("rom_label")
        self.rom_layout.addWidget(self.rom_label)
        self.rom_list = QtWidgets.QListWidget(search_dialog)
        self.rom_list.setObjectName("rom_list")
        self.rom_layout.addWidget(self.rom_list)
        self.main_layout.addLayout(self.rom_layout)
        self.gridLayout.addLayout(self.main_layout, 1, 0, 1, 1)
        self.search_bar_layout = QtWidgets.QHBoxLayout()
        self.search_bar_layout.setObjectName("search_bar_layout")
        self.search_label = QtWidgets.QLabel(search_dialog)
        self.search_label.setFrameShape(QtWidgets.QFrame.Panel)
        self.search_label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.search_label.setObjectName("search_label")
        self.search_bar_layout.addWidget(self.search_label)
        self.search_bar_line_edit = QtWidgets.QLineEdit(search_dialog)
        self.search_bar_line_edit.setObjectName("search_bar_line_edit")
        self.search_bar_layout.addWidget(self.search_bar_line_edit)
        self.search_bar_button = QtWidgets.QPushButton(search_dialog)
        self.search_bar_button.setObjectName("search_bar_button")
        self.search_bar_layout.addWidget(self.search_bar_button)
        self.gridLayout.addLayout(self.search_bar_layout, 0, 0, 1, 1)

        self.retranslateUi(search_dialog)
        self.search_dialog_buttonbox.accepted.connect(search_dialog.accept)
        self.search_dialog_buttonbox.rejected.connect(search_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(search_dialog)

    def retranslateUi(self, search_dialog):
        _translate = QtCore.QCoreApplication.translate
        search_dialog.setWindowTitle(_translate("search_dialog", "Search Roms"))
        self.console_label.setText(_translate("search_dialog", "Console:"))
        self.rom_label.setText(_translate("search_dialog", "Rom :"))
        self.search_label.setText(_translate("search_dialog", "Search:"))
        self.search_bar_button.setText(_translate("search_dialog", "GO!"))

