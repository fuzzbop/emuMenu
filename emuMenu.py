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

from PyQt5 import QtGui, QtWidgets
import sys
import backend
import emuMenuMainWindow
import addConsoleDialog
import addRomDialog
import editCommand
import addRomFile



class edit_command(QtWidgets.QDialog, editCommand.Ui_edit_command_dialog):
	# Dialog to edit commands
	
	def __init__(self, parent=None):
		
		super(edit_command, self).__init__(parent)
		self.setupUi(self)
		self.generate_combo_box()
		self.edit_command_line_edit.setText(backend.console_command(self.console_name_combo.currentText()))
		self.console_name_combo.activated.connect(self.update_choice)
		
	def update_choice(self):
		self.edit_command_line_edit.setText(backend.console_command(self.console_name_combo.currentText()))
		
	def generate_combo_box(self):
		
		self.console_name_combo.clear()
		full_console_list = backend.console_list()
		for console in range(len(backend.console_list())):
			self.console_name_combo.addItem(full_console_list[console][0])
					
	def accept(self):
		backend.edit_console_command(self.console_name_combo.currentText(), self.edit_command_line_edit.text())
		self.close()
		
class add_console(QtWidgets.QDialog, addConsoleDialog.Ui_add_console_dialog):
	# Dialog to get information to add console to database
	
	def __init__(self, parent=None):
		
		super(add_console, self).__init__(parent)
		self.setupUi(self)
		self.hash_open_button.clicked.connect(self.select_file)

	
	def accept(self):
		name = self.console_name_text.text()
		command = self.command_text.text()
		hash_file = self.hash_line_edit.text()
		if self.hash_check_box.isChecked():
			backend.add_console(name, command, hash_file)
		else:
			backend.add_console(name, command, " ")

		self.close()
		
	def select_file(self):
		text = QtWidgets.QFileDialog.getOpenFileName()
		self.hash_line_edit.setText(text[0])
		
class add_roms(QtWidgets.QDialog, addRomDialog.Ui_add_rom_dialog):
	# Dialog to get information to add to rom datbase table
	
	def __init__(self, parent=None):
		super(add_roms, self).__init__(parent)
		self.setupUi(self)
		self.generate_combo_box()
		self.directory_button.clicked.connect(self.select_directory)
		
	def generate_combo_box(self):
		
		self.console_name_combo.clear()
		full_console_list = backend.console_list()
		for console in range(len(backend.console_list())):
			self.console_name_combo.addItem(full_console_list[console][0])
	
	def select_directory(self):
		directory = QtWidgets.QFileDialog.getExistingDirectory()
		self.directory_line_edit.setText(directory)
		
	def accept(self):
		console = self.console_name_combo.currentText()
		directory = self.directory_line_edit.text()
		extension = self.extension_line_edit.text()
		backend.add_games(console, directory, extension)
		self.close()
		
class add_roms_file(QtWidgets.QDialog, addRomFile.Ui_add_rom_file_dialog):
	# Dialog to get information to add to rom datbase table
	
	def __init__(self, parent=None):
		super(add_roms_file, self).__init__(parent)
		self.setupUi(self)
		self.generate_combo_box()
		self.file_button.clicked.connect(self.select_filename)
		self.verify_button.clicked.connect(self.select_verify_filename)
		
	def generate_combo_box(self):
		
		self.console_name_combo.clear()
		full_console_list = backend.console_list()
		for console in range(len(backend.console_list())):
			self.console_name_combo.addItem(full_console_list[console][0])
	
	def select_filename(self):
		filename = QtWidgets.QFileDialog.getOpenFileName()
		self.file_line_edit.setText(filename[0])
		
	def select_verify_filename(self):
		verify_name = QtWidgets.QFileDialog.getOpenFileName()
		self.verify_line_edit.setText(verify_name[0])
		
	def accept(self):
		console = self.console_name_combo.currentText()
		filename_file = self.file_line_edit.text()
		verify_file = self.verify_line_edit.text()
		backend.add_games_hash(console, filename_file, verify_file)
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
		self.action_add_roms_from_file.triggered.connect(self.open_add_roms_file)
		self.action_quit.triggered.connect(self.close)
		self.setWindowIcon(QtGui.QIcon('assets/emu_black_silhouette.svg'))


	def open_add_console(self):
		
		add_console().exec()
		self.generate_console_list()
		
	def open_add_roms(self):
		
		add_roms().exec()
	
	def open_add_roms_file(self):
		
		add_roms_file().exec()
	
	def open_edit_command(self):
		edit_command().exec()
		
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
		command = backend.console_command(console)
		rom_full_path = backend.full_rom_path(console, rom)
		
		# if "<ROM>" in command:
			# command = command.replace("<ROM>", '"' + rom_full_path + '"')
		
		# elif "hbmame <BASENAME>" in command:
			# command = command.replace("<BASENAME>", rom_full_path)
		
		# elif "<BASENAME>" in command:
			# base_name = backend.full_rom_path(console, rom)
			# for slices in range(base_name.count("/")):
				# base_name = base_name[base_name.find("/")+1:]
			# base_name = base_name[:base_name.find(".")]
			# command = command.replace("<BASENAME>", base_name)
		# else:
			# error_dialog = QtWidgets.QErrorMessage()
			# error_dialog.showMessage("<ROM> or <BASENAME> not found in command!")
			
		backend.launch(command, rom_full_path)
		
	def contextMenuEvent(self, event):
		menu = QtWidgets.QMenu(self)
		purge_action = menu.addAction("Purge Roms")
		edit_command = menu.addAction("Change Launch Command")
		action = menu.exec(self.mapToGlobal(event.pos()))
		if action == purge_action:
			self.purge_console_roms()
		elif action == edit_command:
			self.open_edit_command()
		
	def purge_console_roms(self):
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
