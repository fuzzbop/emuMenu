# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'assets/favoritesDialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_favorite_dialog(object):
    def setupUi(self, favorite_dialog):
        favorite_dialog.setObjectName("favorite_dialog")
        favorite_dialog.resize(783, 636)
        self.gridLayout = QtWidgets.QGridLayout(favorite_dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.favorite_dialog_buttonbox = QtWidgets.QDialogButtonBox(favorite_dialog)
        self.favorite_dialog_buttonbox.setOrientation(QtCore.Qt.Horizontal)
        self.favorite_dialog_buttonbox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.favorite_dialog_buttonbox.setObjectName("favorite_dialog_buttonbox")
        self.gridLayout.addWidget(self.favorite_dialog_buttonbox, 1, 0, 1, 1)
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setObjectName("main_layout")
        self.console_layout = QtWidgets.QVBoxLayout()
        self.console_layout.setObjectName("console_layout")
        self.console_label = QtWidgets.QLabel(favorite_dialog)
        self.console_label.setFrameShape(QtWidgets.QFrame.Panel)
        self.console_label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.console_label.setAlignment(QtCore.Qt.AlignCenter)
        self.console_label.setObjectName("console_label")
        self.console_layout.addWidget(self.console_label)
        self.console_list = QtWidgets.QListWidget(favorite_dialog)
        self.console_list.setObjectName("console_list")
        self.console_layout.addWidget(self.console_list)
        self.main_layout.addLayout(self.console_layout)
        self.rom_layout = QtWidgets.QVBoxLayout()
        self.rom_layout.setObjectName("rom_layout")
        self.rom_label = QtWidgets.QLabel(favorite_dialog)
        self.rom_label.setFrameShape(QtWidgets.QFrame.Panel)
        self.rom_label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.rom_label.setAlignment(QtCore.Qt.AlignCenter)
        self.rom_label.setObjectName("rom_label")
        self.rom_layout.addWidget(self.rom_label)
        self.rom_list = QtWidgets.QListWidget(favorite_dialog)
        self.rom_list.setObjectName("rom_list")
        self.rom_layout.addWidget(self.rom_list)
        self.main_layout.addLayout(self.rom_layout)
        self.gridLayout.addLayout(self.main_layout, 0, 0, 1, 1)

        self.retranslateUi(favorite_dialog)
        self.favorite_dialog_buttonbox.accepted.connect(favorite_dialog.accept)
        self.favorite_dialog_buttonbox.rejected.connect(favorite_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(favorite_dialog)

    def retranslateUi(self, favorite_dialog):
        _translate = QtCore.QCoreApplication.translate
        favorite_dialog.setWindowTitle(_translate("favorite_dialog", "Favorites"))
        self.console_label.setText(_translate("favorite_dialog", "Console:"))
        self.rom_label.setText(_translate("favorite_dialog", "Rom :"))

