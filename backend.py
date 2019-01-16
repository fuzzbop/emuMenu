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
import math
import pathlib
import random

pathlib.Path.mkdir(pathlib.PurePath.joinpath(pathlib.Path.home(), ".config/emuMenu"), parents=True, exist_ok=True)
working_dir = pathlib.PurePath.joinpath(pathlib.Path.home(), ".config/emuMenu")
db = lite.connect(pathlib.PurePath.joinpath(working_dir, "games.db"))

def init_db():
	# Function to initialise the database.

	with db:
		cursor = db.cursor()
		cursor.execute("CREATE TABLE IF NOT EXISTS consoles (name TEXT, command TEXT)")
def update_txt(console, rom):
	current_game = open(pathlib.PurePath.joinpath(working_dir, "now_playing.txt"), "w+")
	current_game.truncate()
	current_game.write("Now Playing: " + rom + " on " + console + " \r\n")
	current_game.close

def launch(console, rom):
	# Launches command given from string via subprocess and shlex.
	# Needs rewritten for multiplatform compatibility.

	command = console_command(console)
	rom_full_path = full_rom_path(console, rom)
	update_txt(console, rom)
			
	if "<ROM>" in command:
		command = command.replace("<ROM>", '"' + rom_full_path + '"')

	elif "<BASENAME>" in command:
			base_name = os.path.basename(rom_full_path)
			base_name = base_name.split(".")
			command = command.replace("<BASENAME>", base_name[0])
	else:
		print("Command Not Launchable")
	command = str(pathlib.PurePath(command))
	
	if os.name == "posix":
		subprocess.run(shlex.split(command))
	else:
		subprocess.run(command)

def launch_random():
	consoles = console_list()
	random_number = random.SystemRandom()
	random_console = consoles[random_number.randint(0,len(consoles)-1)][0]
	roms = rom_list(random_console)
	random_rom = roms[random_number.randint(0,len(roms)-1)][0]
	launch(random_console, random_rom)

def text_lines(text_file):
	# Returns and list with the contents of each line of the supplied text file.

	lines = []
	with open(text_file) as input_file:
		for line in input_file:
			lines.append(line)
	return lines

def add_console(name, command):
	# Adds a console to the database, then creates table in database for the new console.

	with db:
		cursor = db.cursor()
		cursor.execute("INSERT INTO consoles VALUES(?,?)", (name, command))
		cursor.execute("CREATE TABLE '" + name + "' (name TEXT, location TEXT, pretty_name TEXT)")

def add_games_directory(console, directory, extension):
	# Adds games from a directory with a given extension to a consoles game table after checking if it exists.
	progress = 0
	counter = 0
	emu = console_command(console)
	with db:
		cursor = db.cursor()

		current_games = rom_location_list(console)
		for filename in glob.iglob(str(pathlib.Path(directory)) + os.sep +'**/*' + extension, recursive=True):
			counter += 1
			progress = math.trunc(counter/len(next(glob.iglob(directory, recursive=True))))*100
			print(progress)
			name = filename[:-(len(extension) + 1)].replace("'","''")
			name = os.path.basename(name)
			location = filename
			if not any(location in test[0] for test in current_games) :
				cursor.execute("INSERT INTO '" + console + "' VALUES(?,?,?)", (name, location, name))

def add_games_hash(console, filename):
	# Adds games from MAME Softlist Hash File
	progress = 0
	counter = 0
	current_games = rom_name_list(console)
	
	tree = et.parse(filename)
	root = tree.getroot()
	length = len(root.findall("software"))
	for software in root.findall("software"):
		counter += 1
		progress = math.trunc(counter/length*100)
		print(progress)		
		name = software.get("name")
		pretty_name = software.find("description").text
		with db:
			if not any(name in test[0] for test in current_games):
				cursor = db.cursor()
				cursor.execute("INSERT INTO '" + console + "' VALUES(?,?,?)", (name, name, pretty_name))

def add_games_files(console, text_file = " ", verify_file = " "):
	# Adds games from verify file, uses text file to get pretty name (written for MAME -listall)
	progress = 0
	counter = 0
	current_games = rom_name_list(console)
	
	file_lines = text_lines(text_file)
	if verify_file is not " ":
		verify_lines = text_lines(verify_file)
	length = len(verify_lines)
	games = dict()
	for name in range(len(file_lines)):
		last_checked = file_lines[name -1].split(" ",1)
		badname = file_lines[name].split(" ", 1)
		command_name = badname[0]
		pretty_name = badname[1]
		pretty_name = pretty_name[pretty_name.find('"'):].split('"')

		if last_checked[0][0] == "z" and command_name[0][0] == "a":
			# Breaks out of loop if list cycles alphabetical, MAME -listall starts
			# over when it gets past software and onto hardware.
			break
		if len(pretty_name) > 1:
			games[command_name] = pretty_name[1]
	for test in range(len(verify_lines)):
		counter += 1
		progress = math.trunc(counter/length*100)
		print(progress)
		verify_split = verify_lines[test].split()
		if verify_split[0] == "romset":
			if games.get(verify_split[1]) is not None:
				if "best" in verify_split or "good" in verify_split:
					if not any(name in exists[0] for exists in current_games):
						with db:
							cursor = db.cursor()
							cursor.execute("INSERT INTO '" + console + "' VALUES(?,?,?)", (verify_split[1], verify_split[1], games.get(verify_split[1])))
		else:
			if ((games.get(verify_lines[test][:-1]) and verify_lines[test]) is not None):
				print("command = " + games.get(verify_lines[test][:-1]))
				print("verify = " + verify_lines[test])
				if not any(name in exists[0] for exists in current_games):
					with db:
						cursor = db.cursor()
						cursor.execute("INSERT INTO '" + console + "' VALUES(?,?,?)", (verify_lines[test][:-1], verify_lines[test][:-1], games.get(verify_lines[test][:-1])))
			#if games.get(test) in verify_lines[test][0]:
			#	with db:
			#		if not any(name in test[0] for test in current_games):
			#			cursor = db.cursor()
						#cursor.execute("INSERT INTO '" + console + "' VALUES(?,?,?)", (command_name, command_name, pretty_name[1]))

def table_length(table):
	# Returns the length of a table.

	with db:
		cursor = db.cursor()
		cursor.execute("SELECT Count(*) FROM '" + table + "'")
		return cursor.fetchall()[0][0]

def console_command(console):
	# Returns command for specified console.

	with db:
		cursor = db.cursor()
		cursor.execute("SELECT command FROM consoles WHERE name IS '" + console + "'")
		return cursor.fetchall()[0][0]

def edit_console_command(console, command):
	# edits command for specified console with specified command.

	with db:
		cursor = db.cursor()
		cursor.execute("UPDATE consoles SET command= ? WHERE name = ?", (command, console))

def clear_roms(console):
	# Removes all enrties for a selected console.

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

def rom_name_list(console):
	# Returns list of roms in supplied console's table

	with db:
		cursor = db.cursor()
		cursor.execute("SELECT name FROM '" + console + "' ORDER BY name")
		return cursor.fetchall()

def rom_list(console):
	# Returns list of roms in supplied console's table

	with db:
		cursor = db.cursor()
		cursor.execute("SELECT pretty_name FROM '" + console + "' ORDER BY pretty_name COLLATE NOCASE ASC")
		return cursor.fetchall()
