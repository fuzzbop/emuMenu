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
import re

pathlib.Path.mkdir(pathlib.PurePath.joinpath(pathlib.Path.home(), ".config/emuMenu"), parents=True, exist_ok=True)
working_dir = pathlib.PurePath.joinpath(pathlib.Path.home(), ".config/emuMenu")
db = lite.connect(pathlib.PurePath.joinpath(working_dir, "games.db"), check_same_thread=False)

# Main Functions

def update_txt(console, rom):
	# Create and/or populate text file with game being launched
	
	current_game = open(pathlib.PurePath.joinpath(working_dir, "now_playing.txt"), "w+")
	current_game.truncate()
	current_game.write("Now Playing: " + rom + " on " + console + " \r\n")
	current_game.close

def launch(console, rom):
	# Launches command given from string via subprocess and shlex.

	command = console_command(console)

	if os.sep in rom:
		rom_full_path = rom
	else:
		rom_full_path = full_rom_path(console, rom)
	update_txt(console, rom)

	if "<ROM>" in command:
		command = command.replace("<ROM>", '"' + rom_full_path + '"')
	elif "<BASENAME>" in command:
		command = command.replace("<BASENAME>", full_rom_path(console, rom))
	else:
		print("Command Not Launchable")
	command = str(pathlib.PurePath(command))

	if os.name == "posix":
		subprocess.run(shlex.split(command))
	else:
		subprocess.run(command)

def launch_random():
	# Launches a random game from a random console.
	
	consoles = console_list()
	random_number = random.SystemRandom()
	random_console = consoles[random_number.randint(0,len(consoles)-1)][0]
	roms = rom_list(random_console)
	random_rom = roms[random_number.randint(0,len(roms)-1)][0]
	launch(random_console, random_rom)
	
def progress(value):
	# Simply holds a percentage variable so it can be called to update GUI progress bars
	
	progress.percentage=value


# Database Edit Functions


def init_db():
	# Function to initialise the database.

	with db:
		cursor = db.cursor()
		cursor.execute("CREATE TABLE IF NOT EXISTS consoles (name TEXT, command TEXT, UNIQUE(name, command))")
		cursor.execute("CREATE TABLE IF NOT EXISTS favorites (pretty_name TEXT, location TEXT, console TEXT, UNIQUE(pretty_name, location, console))")

def add_console(name, command):
	# Adds a console to the database, then creates table in database for the new console.

	with db:
		cursor = db.cursor()
		cursor.execute("INSERT OR IGNORE INTO consoles VALUES(?,?)", (name, command))
		cursor.execute("CREATE TABLE IF NOT EXISTS '" + name + "' (name TEXT, location TEXT, pretty_name TEXT, UNIQUE(name, location, pretty_name))")
		
def add_games_directory(console, directory, extension):
	# Adds games from a directory with a given extension to a consoles game table after checking if it exists.

	progress(1)
	counter = 0
	emu = console_command(console)
	length = len(list(glob.iglob(str(pathlib.Path(directory)) + os.sep +'**/*' + extension, recursive=True)))
	to_insert = [ ]

	for filename in glob.iglob(str(pathlib.Path(directory)) + os.sep +'**/*' + extension, recursive=True):
		counter += 1
		progress((math.trunc(counter/length*100))-1)
		name = filename[:-(len(extension) + 1)]
		name = os.path.basename(name)
		location = filename
		to_insert.append((name, location, name))
	add_games_execute(console, to_insert)
	progress(100)
	
def add_games_hash(console, filename):
	# Adds games from MAME Softlist Hash file after checking is it exists

	progress(0)
	counter = 0
	tree = et.parse(filename)
	root = tree.getroot()
	length = len(root.findall("software"))
	to_insert=[ ]
	
	for software in root.findall("software"):
		counter += 1
		progress((math.trunc(counter/length*100))-1)
		name = software.get("name")
		pretty_name = software.find("description").text
		to_insert.append((name, name, pretty_name))
	
	add_games_execute(console, to_insert)
	progress(100)
	
def add_games_files(console, text_file=" ", verify_file=" "):
    # Adds games from verify file after checking if it exists, uses text file to get pretty name (written for MAME -listall)

	progress(1)
	counter = 0
	
	games = { }
	verified = [ ]

	mames_name = re.compile('^[^\\s]*')
	mames_pretty = re.compile('(?<=\")[^\"]*')
	with open(text_file) as input_file:
		for line in input_file:
			result = mames_name.search(line)
			if result:
				name = result.group(0)
				result = mames_pretty.search(line)
				if result:
					pretty = result.group(0)
					games[name] = (name, name, pretty)
		input_file.close()
		
	length = len(games)
	verify = re.compile('(?<=romset\\s)[^\\s]*(?=.*(good|best).*)')        
	with open(verify_file) as input_file:
		for line in input_file:
			counter += 1           
			progress((math.trunc(counter/length*100))-1)
			result = verify.search(line)        
			if result:
				name = result.group(0)
				entry = games[name]
				if entry:
					verified.append((entry[0], entry[1], entry[2]))
		input_file.close()
	
	add_games_execute(console, verified)
	progress(100)
	
def add_games_execute(console, list):
	# Actual SQL call for the above functions

	with db:
		cursor = db.cursor()
		cursor.executemany("INSERT OR IGNORE INTO '" + console + "' VALUES(?,?,?)", list)
		
def clear_roms(console):
	# Removes all enrties for a selected console.

	with db:
		cursor = db.cursor()
		cursor.execute("DELETE FROM '" + console + "'")
		
def add_favorite(console, rom):
	# Adds rom to favorites database table.

	location = full_rom_path(console, rom)
	with db:
		cursor = db.cursor()
		cursor.execute("INSERT OR IGNORE INTO favorites VALUES(?,?,?)", (rom, location, console))

def remove_favorite(console, rom):
		# Remove rom from favorites database table.
		
	with db:
		cursor = db.cursor()
		cursor.execute("DELETE FROM favorites WHERE console=? AND pretty_name=?", (console, rom))
		
def remove_console(console):
		# Remove rom from favorites database table.
		
	with db:
		cursor = db.cursor()
		cursor.execute("DELETE FROM consoles WHERE name=?", (console,))
		cursor.execute("DROP TABLE '" + console + "'")
		
def edit_console_command(console, command):
	# edits command for specified console with specified command.

	with db:
		cursor = db.cursor()
		cursor.execute("UPDATE consoles SET command= ? WHERE name = ?", (command, console))


# Database Queries 		


def table_length(table):
	# Returns the length of a table.

	with db:
		cursor = db.cursor()
		cursor.execute("SELECT Count(*) FROM '" + table + "'")
		return cursor.fetchall()[0][0]

def console_list():
	# Returns all consoles in the database

	with db:
		cursor = db.cursor()
		cursor.execute("SELECT name FROM consoles ORDER BY name")
		return cursor.fetchall()
		
def console_command(console):
	# Returns command for specified console.

	with db:
		cursor = db.cursor()
		cursor.execute("SELECT command FROM consoles WHERE name IS '" + console + "'")
		return cursor.fetchall()[0][0]
		
def full_rom_path(console, rom):
	# Returns full rom path for supplied rom for supplied console

	with db:
		cursor = db.cursor()
		cursor.execute("SELECT location FROM '"+ console + "' WHERE pretty_name IS '" + rom.replace("'", "''") + "'")
		return cursor.fetchall()[0][0]

def rom_list(console):
	# Returns list of roms in supplied console's table

	with db:
		cursor = db.cursor()
		cursor.execute("SELECT pretty_name FROM '" + console + "' ORDER BY pretty_name COLLATE NOCASE ASC")
		return cursor.fetchall()
		
def rom_location_list(console):
	# Returns list of roms by location for checking if roms allready in list

	with db:
		cursor = db.cursor()
		cursor.execute("SELECT location FROM '" + console + "' ORDER BY location")
		return cursor.fetchall()
		
def rom_name_list(console):
	# Returns list of roms in supplied console's table

	with db:
		cursor = db.cursor()
		cursor.execute("SELECT name FROM '" + console + "'")
		return cursor.fetchall()
		
def favorite_console_list():
	# Generate list of consoles in favorites database

	with db:
		cursor = db.cursor()
		cursor.execute("SELECT console FROM favorites ORDER BY console")
		return cursor.fetchall()

def favorite_rom_list(console):
	# Generates full rom list from favorites database
	
	with db:
		cursor = db.cursor()
		cursor.execute("SELECT pretty_name FROM favorites WHERE console='" + console +"' ORDER BY pretty_name")
		return cursor.fetchall()
		
def search_roms(search):
	# Searches rom names in database for search term provided.
	
	with db:
		cursor = db.cursor()
		cursor.execute("SELECT name FROM sqlite_master WHERE type='table'" )
		console_list = cursor.fetchall()
		results = []
		
		for test in range(len(console_list)):		
			if "consoles" not in console_list[test][0]:
				cursor.execute("SELECT pretty_name FROM '" + console_list[test][0] + "' WHERE pretty_name LIKE ?", ("%" + search + "%",))
				raw_results = cursor.fetchall()
				if raw_results:
					results.append(console_list[test][0])
					results.append(raw_results)
		return results
