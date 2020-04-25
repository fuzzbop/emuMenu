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
* Your database and currently playing textfile will be held in $HOME/.config/emuMenu
* Run with python emuMenu.py

### Windows:

* Install Python 3 https://www.python.org/downloads/ be sure to check PATH option during install
* Install Qt https://www.qt.io/download-qt-installer
* Install PyQt5 type "python -m pip install PyQt5" into command line (search cmd when you open start menu)
* Your database and currently playing textfile will be held in C:\users\<your username>\.config\emuMenu
* Run by opening emuMenu.py

### Mac:
* Fuck if I know, but it should work in theory

## HOW TO Use:

A default database will be created when you first open the program.

* You must add a console before you add any games.
* Hit the Add Console menu item, and give the console a name (you can name it anything.)
* In the second line you need to type out the command to launch the rom using \<ROM\> and \<BASENAME\> to designate where to put the rom information pulled from the database. 
* \<ROM\> is a full path to a rom file, \<BASENAME\> is just the name of the file without the path or extension (Useful for MAME).
* \<ROM\> Example: `retroarch -L /path/to/core.so <ROM>`
* \<BASENAME\> Example: `mame <BASENAME>`

After you add your console, you need to add some roms. There are currently three implemented ways to do this with the Add Roms menu item.
* If you check Playlist, you provide a Retroarch Playlist .lpl file.
* If you check Hash, you provide the hash file for the MAME softlist (currently adds full list, dosent check for avaliablity).
* If you check Directory and Extension, you provide a directory with the open button, and type in your extension (without the .). Can also check Hash and provide a MAME Hash for pretty names!
* If you check listfull and either verify or custom: You provide the output of mame -listfull to listfull, the output of mame -verify or a custom list of roms (In the style of MFM, so a basename for each mame rom you would like on each line of the txt file.)

The -listfull and -verify option takes quite a while to run (around 20 min)
Now you will have a list of consoles on the left pane and roms on the right pane. These are all generated on the fly.

You can purge roms for a console by right clicking the console and selecting purge roms. You can edit the console's command as well.

There is a favorites list implemented, to add a rom to favorites, right click the rom you want to add and select add rom to favorites.
When you press the favorites button on the main UI a window will pop up that mimics the main windows console-rom split that has the favorites
implemented.

There is a search feature implemented, when you press the search button on the main UI a window that mimics the main windows console-rom split
will pop up that has a search bar above it, when you search a term all results in the database will be entered into the new windows lists.


## Screenshots
### Main Screen
<img src=https://i.imgur.com/wFSral2.png width=300>

### Search Screen
<img src=https://i.imgur.com/24jXCAp.png width=300>

### Favorites Screen
<img src=https://i.imgur.com/05rPSNo.png width=300>

### Add Console
<img src=https://i.imgur.com/SC1fNsr.png width=500>
<img src=https://i.imgur.com/Ga7h9RT.png width=500>

### Add Roms
<img src=https://i.imgur.com/CorLrO5.png width=500>
<img src=https://i.imgur.com/vThyqeW.png width=500>


## TODO:
* ~~Handle merged MAME rom sets, and custom rom lists for MAME~~
* ~~Create favorites database and window~~
* ~~Implement progress bars~~
* Clean up various parts of the GUI
* More features as I think of them or get suggestions
* Clean up code
* Optimise code and module usage (likely never ending)


## Wayout TO-DO:
* simple fullscreen gui possible

