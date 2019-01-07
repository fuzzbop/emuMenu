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

import subprocess
import shlex
import sqlite3 as lite
import glob
import xml.etree.ElementTree as et
import os


db = lite.connect("games.db")

def init_db():
	# Function to initialise the database.
	
	with db:
		cursor = db.cursor()
		cursor.execute("CREATE TABLE IF NOT EXISTS consoles (name TEXT, command TEXT, hash_file TEXT)")

def launch(command, rom_full_path):
	# Launches command given from string via subprocess and shlex

	if "<ROM>" in command:
		command = command.replace("<ROM>", '"' + rom_full_path + '"')
		
	elif "<BASENAME>" in command:
			base_name = os.path.basename(rom_full_path)
			base_name = base_name.split(".")
			command = command.replace("<BASENAME>", base_name[0])
	else:
		print("Command Not Launchable")
	
	subprocess.run(shlex.split(os.fsdecode(command)))

def find_pretty_name(test, console, hash_file_lines):
	# Tests command for <BASENAME> command format, then returns the pretty name based on the hash/txt file supplied

	if "mame <BASENAME>" in console:
		for name in range(len(hash_file_lines)):
			badname = hash_file_lines[name].split(" ", 1)
		
			if badname[0] == test:
				pretty_name = badname[1]
				pretty_name = pretty_name[pretty_name.find('"'):].split('"')   # removes leading spaces
				return pretty_name[1]


	elif "<BASENAME>" in console:
		xml = hash_file(console)
		tree = et.parse(xml)
		root = tree.getroot()

		for software in root.findall("software"):
			name = software.get("name")
			pretty_name = software.find("description").text

			if name == test:
				if pretty_name is not None:
					return pretty_name
				else:
					return test

	else:
		return test.replace("''", "'")

def hash_lines(hash_file):
	# returns and list with the contents of each line of the supplied hash_file
	
	lines = []
	with open(hash_file) as input_file:
		for line in input_file:
			lines.append(line)
	return lines
	
def hash_file(console):
	# Returns hash file for specified console
	
	with db:
		cursor = db.cursor()
		cursor.execute("SELECT hash_file FROM consoles WHERE command IS '" + console +"'")
		return cursor.fetchall()[0][0]

def add_console(name, command, hash_file):
	# Adds a console to the database, then creates table in database for the new console

	with db:
		cursor = db.cursor()
		cursor.execute("INSERT INTO consoles VALUES(?,?,?)", (name, command, hash_file))
		cursor.execute("CREATE TABLE '" + name + "' (name TEXT, location TEXT, pretty_name TEXT)")

def add_games(console, directory, extension):
	# Adds games from a directory with a given extension to a consoles game table after checking if it exists

	emu = console_command(console)
	
	if hash_file(emu) is not " ":
		hash_file_lines = hash_lines(hash_file(emu))
	else:
		hash_file_lines = " "
	
	with db:
		cursor = db.cursor()
	
		current_games = rom_location_list(console)
		for filename in glob.iglob(directory + '/**/*' + extension, recursive=True):
			name = filename[:-len(extension)-1].replace("'","''")

			#for slices in range(name.count("/")):
			#	name = name[name.find("/")+1:]
			name = os.path.basename(name)
			location = filename
			pretty_name = find_pretty_name(name, emu, hash_file_lines)
			if not any(location in test[0] for test in current_games) :
				cursor.execute("INSERT INTO '" + console + "' VALUES(?,?,?)", (name, location, pretty_name))

def add_games_hash(console, filename, verify_file = "None"):

	if ".xml" in filename:
		xml = hash_file(console)
		tree = et.parse(xml)
		root = tree.getroot()

		for software in root.findall("software"):
			name = software.get("name")
			pretty_name = software.find("description").text
			with db:
				cursor = db.cursor()
				cursor.execute("INSERT INTO '" + console + "' VALUES(?,?,?)", (name[0], name[0], pretty_name[1]))
	else:
		file_lines = hash_lines(filename)
		
		if verify_file is not "None":
			verify_lines = hash_lines(verify_file)
			
		for name in range(len(file_lines)):
			last_checked = file_lines[name -1].split(" ",1)
			badname = file_lines[name].split(" ", 1)
			command_name = badname[0]
			pretty_name = badname[1]
			pretty_name = pretty_name[pretty_name.find('"'):].split('"')
			
			if last_checked[0][0] == "z" and command_name[0][0] == "a":
				break
			if len(pretty_name) > 1:
				for test in range(len(verify_lines)):
					if command_name in verify_lines[test]:
						with db:
							cursor = db.cursor()
							cursor.execute("INSERT INTO '" + console + "' VALUES(?,?,?)", (command_name, command_name, pretty_name[1]))

def table_length(table):
	# Returns the length of a table

	with db:
		cursor = db.cursor()
		cursor.execute("SELECT Count(*) FROM '" + table + "'")
		return cursor.fetchall()[0][0]

def console_command(console):
	# Returns command for specified console
	with db:
		cursor = db.cursor()
		cursor.execute("SELECT command FROM consoles WHERE name IS '" + console + "'")
		return cursor.fetchall()[0][0]

def edit_console_command(console, command):
	# edits command for specified console with specified command
	
	with db:
		cursor = db.cursor()
		cursor.execute("UPDATE consoles SET command= ? WHERE name = ?", (command, console))

def clear_roms(console):
	with db:
		cursor = db.cursor()
		cursor.execute("DELETE FROM '" + console + "'")

def full_rom_path(console, rom):
	# Returns full rom path for supplied rom for supplied console

	with db:
		cursor = db.cursor()
		cursor.execute("SELECT location FROM '"+ console + "' WHERE pretty_name IS '" + rom.replace("'", "''") + "'")
		return cursor.fetchall()[0][0]

def console_list():
	# Returns all consoles in the database

	with db:
		cursor = db.cursor()
		cursor.execute("SELECT name FROM consoles ORDER BY name")
		return cursor.fetchall()

def rom_location_list(console):
	# returns list of roms by location for checking if roms allready in list
	
	with db:
		cursor = db.cursor()
		cursor.execute("SELECT location FROM '" + console + "' ORDER BY location")
		return cursor.fetchall()

def rom_list(console):
	# Returns list of roms in supplied console's table

	with db:
		cursor = db.cursor()
		cursor.execute("SELECT pretty_name FROM '" + console + "' ORDER BY pretty_name")
		return cursor.fetchall()
