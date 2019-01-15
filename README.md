# emuMenu
<img src="assets/emu_black_silhouette.svg/" height="150">

emuMenu is a simple emulator launcher

requirements are python3, python3-sqlite3, python3-qt5


I wanted a simple launcher without all the fluff for those of us with huge collections. I tried to write
this with large collections in mind, but it is also the first thing I have written in a large number of 
years. There may be bad practice and things in place and it is very much so a work in progress.

## HOW TO Install:
	
### Linux:
* Install your distributions packages for python3 and python3-PyQt5
* currently your database and the contents for the project should be housed in the same directory
* run with python emuMenu.py

### Windows:

* Install Python 3 https://www.python.org/downloads/ be sure to check PATH option during install
* Install Qt https://www.qt.io/download-qt-installer
* Install PyQt5 "python -m pip install PyQt5"
		
### Mac:
* Fuck if I know, but it should work in theory

## HOW TO Use:
A default database will be created when you first open the program. 

* You must add a console before you add any games.  
	* Hit the Add Console menu item, and give the console a name (you can name it anything.) 
	* In the second line you need to type out the command to launch the rom using <ROM> and <BASENAME> to designate where to put the rom information pulled from the database. 
<ROM> is a full path to a rom file, <BASENAME> is just the name of the file without the path or extension (Useful for MAME).

After you add your console, you need to add some roms. There are currently three implemented ways to do this with the Add Roms menu item.
* If you check Hash, you provide the hash file for the MAME softlist (currently adds full list, dosent check for avaliablity).
* If you check Directory and Extension, you provide a directory with the open button, and type in your extension (without the .).
* If you check listfull and either verify or custom: You provide the output of mame -listfull to listfull, the output of mame -verify or a custom list of roms (In the style of MFM, so a basename for each mame rom you would like on each line of the txt file.)
	   
The -listfull and -verify option takes quite a while to run (around 20 min) 
Now you will have a list of consoles on the left pane and roms on the right pane. these are all generated on the fly. 

You can purge roms for a console by right clicking the console and selecting purge roms. you can edit the console's command as well.


## TODO:
* make this read-me better
* make sql calls better
* ~~take out manual work around that i have in place for hbmame since it is a merged set~~
* ~~handle merged mame rom sets, and custom rom lists for mame~~
* more stuff as I think about it

## Wayout TO-DO:
* simple fullscreen gui possible

