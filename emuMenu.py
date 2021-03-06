#!/usr/bin/env python3
# emuMenu - A Simple Emulator Frontend
# Copyright (C) 2019 James Sparks II
#
# emuMenu is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from PyQt5 import QtGui, QtWidgets, QtCore
from threading import Thread
import sys
import backend
import emuMenuMainWindow
import addConsoleDialog
import addRomDialog
import editCommand
import customRomDialog
import searchDialog
import favoritesDialog

class edit_command(QtWidgets.QDialog, editCommand.Ui_edit_command_dialog):
	# Dialog to edit commands

	def __init__(self, parent=None):

		super(edit_command, self).__init__(parent)
		self.setupUi(self)
		self.generate_combo_box()
		self.edit_command_line_edit.setText(backend.console_command(self.console_name_combo.currentText()))
		self.console_name_combo.activated.connect(self.update_choice)

	def update_choice(self):
		# Updates text input with the command in database for selected console.

		self.edit_command_line_edit.setText(backend.console_command(self.console_name_combo.currentText()))

	def generate_combo_box(self):
		# Generates console list for combo box

		self.console_name_combo.clear()
		full_console_list = backend.console_list()
		for console in range(len(backend.console_list())):
			self.console_name_combo.addItem(full_console_list[console][0])

	def accept(self):
		# Edits command in the database for the specified console.

		backend.edit_console_command(self.console_name_combo.currentText(), self.edit_command_line_edit.text())
		self.close()

class add_console(QtWidgets.QDialog, addConsoleDialog.Ui_add_console_dialog):
	# Dialog to get information to add console to database

	def __init__(self, parent=None):

		super(add_console, self).__init__(parent)
		self.setupUi(self)


	def accept(self):
		# Adds Console to Database.

		name = self.console_name_text.text()
		command = self.command_text.text()
		backend.add_console(name, command)
		self.close()

class add_roms(QtWidgets.QDialog, addRomDialog.Ui_add_rom_dialog):
	# Dialog to get information to add to rom datbase table

	def __init__(self, parent=None):
		super(add_roms, self).__init__(parent)
		self.setupUi(self)
		self.generate_combo_box()
		self.directory_button.clicked.connect(self.select_directory)
		self.hash_button.clicked.connect(self.select_hash)
		self.listfull_button.clicked.connect(self.select_listfull)
		self.verify_button.clicked.connect(self.select_verify)
		self.custom_button.clicked.connect(self.select_mame_custom)
		self.playlist_button.clicked.connect(self.select_playlist)

	def generate_combo_box(self):
		# Generates console list for combo box.

		self.console_name_combo.clear()
		full_console_list = backend.console_list()
		for console in range(len(backend.console_list())):
			self.console_name_combo.addItem(full_console_list[console][0])

	# Below select_* below opens dialog box and populates text input with selected file

	def select_directory(self):
		directory = QtWidgets.QFileDialog.getExistingDirectory()
		self.directory_line_edit.setText(directory)

	def select_hash(self):
		hash_location = QtWidgets.QFileDialog.getOpenFileName()
		self.hash_line_edit.setText(hash_location[0])
	
	def select_playlist(self):
		playlist_location = QtWidgets.QFileDialog.getOpenFileName()
		self.playlist_line_edit.setText(playlist_location[0])

	def select_listfull(self):
		listfull = QtWidgets.QFileDialog.getOpenFileName()
		self.listfull_line_edit.setText(listfull[0])

	def select_verify(self):
		verify = QtWidgets.QFileDialog.getOpenFileName()
		self.verify_line_edit.setText(verify[0])

	def select_mame_custom(self):
		custom = QtWidgets.QFileDialog.getOpenFileName()
		self.custom_line_edit.setText(custom[0])

	def accept(self):
		# Adds roms from the database from selected options.
		# Currently used combinations are:
		# Hash file only
		# Directory and Extension
		# MAME -listfull output and -verify output
		# MAME custom list and -listfull output

		console = self.console_name_combo.currentText()
		directory = self.directory_line_edit.text()
		extension = self.extension_line_edit.text()
		hash_file = self.hash_line_edit.text()
		listfull_file = self.listfull_line_edit.text()
		verify_file = self.verify_line_edit.text()
		mame_custom_file = self.custom_line_edit.text()
		playlist_file = self.playlist_line_edit.text()
		if ((self.directory_checkbox.isChecked() and self.extension_checkbox.isChecked())
			and not (self.hash_checkbox.isChecked()
			or self.listfull_checkbox.isChecked()
			or self.custom_checkbox.isChecked()
			or self.playlist_checkbox.isChecked()
			or self.verify_checkbox.isChecked())):
			add_thread = Thread(target = backend.add_games_directory, args = (console, directory, extension))
			add_thread.start()
			while add_thread.is_alive():
				self.add_roms_progress.setValue(backend.progress.percentage)
		elif ((self.directory_checkbox.isChecked() and self.extension_checkbox.isChecked() and self.hash_checkbox.isChecked())
			and not (self.verify_checkbox.isChecked()
			or self.listfull_checkbox.isChecked()
			or self.custom_checkbox.isChecked()
			or self.playlist_checkbox.isChecked())):
			add_thread = Thread(target = backend.add_games_directory_hash, args = (console, directory, extension, hash_file))
			add_thread.start()
			while add_thread.is_alive():
				self.add_roms_progress.setValue(backend.progress.percentage)
		elif (self.playlist_checkbox.isChecked()
			and not (self.hash_checkbox.isChecked()
			or self.extension_checkbox.isChecked()
			or self.listfull_checkbox.isChecked()
			or self.verify_checkbox.isChecked()
			or self.custom_checkbox.isChecked()
			or self.directory_checkbox.isChecked())):
			add_thread = Thread(target = backend.add_games_playlist, args = (console, playlist_file))
			add_thread.start()
			while add_thread.is_alive():
				self.add_roms_progress.setValue(backend.progress.percentage)
		elif (self.hash_checkbox.isChecked()
			and not (self.directory_checkbox.isChecked()
			or self.extension_checkbox.isChecked()
			or self.playlist_checkbox.isChecked()
			or self.listfull_checkbox.isChecked()
			or self.custom_checkbox.isChecked()
			or self.verify_checkbox.isChecked())):
			add_thread = Thread(target = backend.add_games_hash, args = (console, hash_file))
			add_thread.start()
			while add_thread.is_alive():
				self.add_roms_progress.setValue(backend.progress.percentage)
		elif ((self.listfull_checkbox.isChecked() and self.verify_checkbox.isChecked())
			and not (self.hash_checkbox.isChecked()
			or self.directory_checkbox.isChecked()
			or self.playlist_checkbox.isChecked()
			or self.extension_checkbox.isChecked()
			or self.custom_checkbox.isChecked())):
			add_thread = Thread(target = backend.add_games_files, args = (console, listfull_file, verify_file))
			add_thread.start()
			while add_thread.is_alive():
				self.add_roms_progress.setValue(backend.progress.percentage)
		elif ((self.listfull_checkbox.isChecked() and self.custom_checkbox.isChecked())
			and not (self.hash_checkbox.isChecked()
			or self.directory_checkbox.isChecked()
			or self.playlist_checkbox.isChecked()
			or self.extension_checkbox.isChecked()
			or self.verify_checkbox.isChecked())):
			add_thread = Thread(target = backend.add_games_files, args = (console, listfull_file, mame_custom_file))
			add_thread.start()
			while add_thread.is_alive():
				self.add_roms_progress.setValue(backend.progress.percentage)
		else:
			error = QtWidgets.QMessageBox()
			error.setIcon(QtWidgets.QMessageBox.Critical)
			error.setWindowTitle("Error")
			error.setText("Invalid Combination")
			error.exec()
					
class custom_roms(QtWidgets.QDialog, customRomDialog.Ui_launch_rom_dialog):
	# Allows user to specify rom location, so it dosent need to be added to the database
	
	def __init__(self, console, parent=None):
		super(custom_roms, self).__init__(parent)
		self.console = console
		self.setupUi(self)
		self.rom_location_button.clicked.connect(self.select_rom)
		
	def select_rom(self):
		rom_location = QtWidgets.QFileDialog.getOpenFileName()
		self.rom_location_line_edit.setText(rom_location[0])
	
	def accept(self):
		backend.launch(self.console, self.rom_location_line_edit.text())
		self.close()
		
class favorite_roms(QtWidgets.QDialog, favoritesDialog.Ui_favorite_dialog):
	# Allows user to specify rom location, so it dosent need to be added to the database
	
	def __init__(self, parent=None):
		super(favorite_roms, self).__init__(parent)
		self.setupUi(self)
		self.console_list.itemClicked.connect(self.generate_rom_list)
		self.rom_list.itemDoubleClicked.connect(self.launch)
		self.rom_list.installEventFilter(self)
		self.generate_consoles()
		
	def generate_consoles(self):
		favorites_console_list = backend.favorite_console_list()
		for console in range(len(favorites_console_list)):
			if not self.console_list.findItems(favorites_console_list[console][0], QtCore.Qt.MatchExactly):
				self.console_list.addItem(favorites_console_list[console][0])
	
	def generate_rom_list(self):

		console = self.console_list.currentItem().text()
		self.rom_list.clear()
		full_rom_list = backend.favorite_rom_list(console)
		for rom in range(len(full_rom_list)):
			self.rom_list.addItem(full_rom_list[rom][0])
		
		
	def eventFilter(self, source, event):
		if (event.type() == QtCore.QEvent.ContextMenu and source is self.rom_list):
			menu = QtWidgets.QMenu()
			purge_action = menu.addAction("Remove From Favorites")
			if menu.exec_(event.globalPos()) == purge_action:
				backend.remove_favorite(self.console_list.currentItem().text(), self.rom_list.currentItem().text())
				self.generate_rom_list()
		return super(favorite_roms, self).eventFilter(source, event)
	
	def launch(self):
		backend.launch(self.console_list.currentItem().text(), self.rom_list.currentItem().text())
					
class search_roms(QtWidgets.QDialog, searchDialog.Ui_search_dialog):
	# Allows user to search database for rom name.
	
	def __init__(self, parent=None):
		super(search_roms, self).__init__(parent)
		self.setupUi(self)
		self.search_bar_button.clicked.connect(self.search_generate_consoles)
		self.console_list.itemClicked.connect(self.search_generate_roms)
		self.rom_list.itemDoubleClicked.connect(self.launch)


	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Return:
			self.search_generate_consoles()

	def search_generate_consoles(self):
		self.console_list.clear()
		self.rom_list.clear()
		result_list = backend.search_roms(self.search_bar_line_edit.text())
		for x in range(len(result_list)):
			if x%2 == 0:
				self.console_list.addItem(result_list[x])

	def search_generate_roms(self):
		self.rom_list.clear()
		selected_console = self.console_list.currentItem().text()
		result_list = backend.search_roms(self.search_bar_line_edit.text())
		for x in range(len(result_list[result_list.index(selected_console)+1])):
			self.rom_list.addItem(result_list[result_list.index(selected_console)+1][x][0])
			
	def launch(self):
		console = self.console_list.currentItem().text()
		rom = self.rom_list.currentItem().text()
		backend.launch(console, rom)

	def accept(self):
		self.close()

class emuMenu(QtWidgets.QMainWindow, emuMenuMainWindow.Ui_emumenu_main_window):

	def __init__(self, parent=None):

		super(emuMenu, self).__init__(parent)
		self.setupUi(self)
		self.generate_console_list()
		self.console_list_widget.itemClicked.connect(self.generate_rom_list)
		self.rom_list_widget.itemDoubleClicked.connect(self.launch_rom)
		self.action_add_console.triggered.connect(self.open_add_console)
		self.action_add_roms.triggered.connect(self.open_add_roms)
		self.action_edit_console_command.triggered.connect(self.open_edit_command)
		self.action_quit.triggered.connect(self.close)
		self.random_button.clicked.connect(backend.launch_random)
		self.search_button.clicked.connect(self.open_search_roms)
		self.favorites_button.clicked.connect(self.open_favorite_roms)
		self.setWindowIcon(QtGui.QIcon('assets/emu_black_silhouette.svg'))
		self.console_list_widget.installEventFilter(self)
		self.rom_list_widget.installEventFilter(self)
		
	def open_search_roms(self):
		
		search_roms().exec()
		
	def open_add_console(self):

		add_console().exec()
		self.generate_console_list()

	def open_add_roms(self):

		add_roms().exec()

	def open_add_roms_file(self):

		add_roms_file().exec()

	def open_edit_command(self):
		edit_command().exec()

	def open_favorite_roms(self):
		favorite_roms().exec()
	
	def resize_console_list(self):

		self.console_label.setMaximumWidth(self.console_list_widget.sizeHintForColumn(0) + 25)
		self.console_list_widget.setMaximumWidth(self.console_list_widget.sizeHintForColumn(0) + 25)

	def generate_console_list(self):
		# Generates console list for console list widget, then calls for layout resize

		self.console_list_widget.clear()
		full_console_list = backend.console_list()
		for console in range(len(full_console_list)):
			self.console_list_widget.addItem(full_console_list[console][0])
		self.resize_console_list()

	def generate_rom_list(self):
		# Generates a rom list from selected consoles database for the rom list widget

		console = self.console_list_widget.currentItem().text()
		self.rom_list_widget.clear()
		full_rom_list = backend.rom_list(console)
		for rom in range(len(full_rom_list)):
			self.rom_list_widget.addItem(full_rom_list[rom][0])	
		self.status_bar.showMessage(str(backend.table_length(self.console_list_widget.currentItem().text())) + " Games")

	def launch_rom(self):
		# Passes command to back end to launch selected rom 

		console = self.console_list_widget.currentItem().text()
		rom = self.rom_list_widget.currentItem().text()
		backend.launch(console, rom)

	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Return:
			self.launch_rom()
			
	def eventFilter(self, source, event):
		if (event.type() == QtCore.QEvent.ContextMenu and source is self.console_list_widget):
			menu = QtWidgets.QMenu()
			purge_action = menu.addAction("Purge Roms")
			edit_command = menu.addAction("Change Launch Command")
			custom_rom = menu.addAction("Launch Custom Rom")
			remove = menu.addAction("Remove Console")

			if menu.exec_(event.globalPos()) == purge_action:
				self.purge_console_roms()
			elif menu.exec_(event.globalPos())== edit_command:
				self.open_edit_command()
			elif menu.exec_(event.globalPos()) == custom_rom:
				self.open_custom_rom()
			elif menu.exec_(event.globalPos()) == remove:
				self.remove_console()
				self.generate_console_list()

		elif (event.type() == QtCore.QEvent.ContextMenu and source is self.rom_list_widget):
			menu = QtWidgets.QMenu(self)
			add_favorite = menu.addAction("Add Rom To Favorites")
			if menu.exec_(event.globalPos()) == add_favorite:
				self.add_to_favorites()
					
		return super(emuMenu, self).eventFilter(source, event)
	
	def remove_console(self):
		backend.remove_console(self.console_list_widget.currentItem().text())

	def open_custom_rom(self):
		# Opens specified rom 
		
		custom_roms(self.console_list_widget.currentItem().text()).exec()
		
	def add_to_favorites(self):
		# Adds selected rom to favorites
		backend.add_favorite(self.console_list_widget.currentItem().text(), self.rom_list_widget.currentItem().text())

	def purge_console_roms(self):
		# Passes console to backend to remove all roms in database

		backend.clear_roms(self.console_list_widget.currentItem().text())
		self.rom_list_widget.clear()

def main():

	backend.init_db()
	app = QtWidgets.QApplication(sys.argv)
	form = emuMenu()
	form.show()
	app.exec()

if __name__ == '__main__':
	main()
