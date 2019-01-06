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

db = lite.connect("games.db")

def init_db():
	# Function to initialise the database.
	
	with db:
		cursor = db.cursor()
		cursor.execute("CREATE TABLE IF NOT EXISTS consoles (name TEXT, command TEXT, hash_file TEXT)")

def launch(command):
	# Launches command given from string via subprocess and shlex

	subprocess.run(shlex.split(command))

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
	# Adds games from a directory with a given extension to a consoles game table

	emu = console_command(console)
	
	if hash_file(emu) is not " ":
		hash_file_lines = hash_lines(hash_file(emu))
	else:
		hash_file_lines = " "
	
	with db:
		cursor = db.cursor()
	
		if "hbmame <BASENAME>" in emu:
			for line in range(len(hash_file_lines[1:9141])):
				name = hash_file_lines[line+1].split(" ", 1)
				pretty_name = name[1]
				pretty_name = pretty_name[pretty_name.find('"'):].split('"')
				
				cursor.execute("INSERT INTO '" + console + "' VALUES(?,?,?)", (name[0], name[0], pretty_name[1]))

		else:
			current_games = rom_location_list(console)
			for filename in glob.iglob(directory + '/**/*' + extension, recursive=True):
				name = filename[:-len(extension)-1].replace("'","''")

				for slices in range(name.count("/")):
					name = name[name.find("/")+1:]
				location = filename
				pretty_name = find_pretty_name(name, emu, hash_file_lines)
				if not any(location in test[0] for test in current_games) :
					cursor.execute("INSERT INTO '" + console + "' VALUES(?,?,?)", (name, location, pretty_name))

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
