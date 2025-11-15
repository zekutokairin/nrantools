#!/usr/bin/env python3

import os
import sys
import datetime
import shutil
import re

import pandas as pd

# TODO: Okay, new plan: we copy all ROMs and Labels and make a new pack directory that's ready to copy in 
#           to the NRAN COntent directory. Lastly, read the original CSV and append the new one with the 
#           lines that correspond to our new files we're adding.

DEBUG = os.getenv("NRAN_DEBUG")

#NRAN_CONTENT_DIR = os.getenv("NRAN_CONTENT_DIR")
NRAN_CONTENT_DIR = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\New Retro Arcade Neon\\NewRetroArcade\\Content"

#PACKDIR = "/Users/user/Sync/Streaming/Games/NRAN/Zekupack/ROMs/cartridges"
#PACKDIR = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\New Retro Arcade Neon\\NewRetroArcade"

PACKDIR = os.getenv("NRAN_PACK")
if not PACKDIR:
    raise Exception("Need to define NRAN_PACK environment variable with your pack directory!")

# Where our new, ready to paste into Content/ pack will go
outputdir = "output"
romdir = os.path.join(outputdir, "Roms")
artdir = os.path.join(outputdir, "Cartridges")
backupdir = os.path.join(outputdir,"backups")
# Make the directories if they don't exist already
os.makedirs("output", exist_ok=True)
os.makedirs(romdir, exist_ok=True)
os.makedirs(artdir, exist_ok=True)
os.makedirs(backupdir, exist_ok=True)

NES_CORE = "bnes_libretro.dll" 
SNES_CORE = "bsnes_performance_libretro.dll" 
GEN_CORE = "picodrive_libretro.dll"
GBA_CORE = "mgba_libretro.dll"

CORE_DICT = {"smc":SNES_CORE,
            "sfc":SNES_CORE,
            "nes":NES_CORE,
            "gg":GEN_CORE,
            "gba":GBA_CORE,
            "md":GEN_CORE}

IMGTYPES = ["jpg","jpeg","png","dds"]

def backupConfigs():
    d = datetime.datetime.now()
    timestamp = "%04d%02d%02d_%02d%02d" % (d.year, d.month, d.day, d.hour, d.minute) 
    currentbackup = os.path.join(backupdir, timestamp)

    os.makedirs(backupdir, exist_ok = True)
    os.makedirs(currentbackup, exist_ok = True)

    import code
    #code.interact(local=locals())
    for f in os.listdir(NRAN_CONTENT_DIR):
        extension = os.path.splitext(f)[1].lower()[1:]
        if extension in ["ini","xml","csv"]:
            shutil.copyfile(os.path.join(NRAN_CONTENT_DIR,f), os.path.join(currentbackup,f))

def getGameName(romname):
    # TODO: Refactor this into the findcartridgelabel to eliminate dupe code
    regex = r"(.*?)(?=\()"
    # At this point, romname is something like 
    #   'Tiny Toon Adventures - Scary Dreams (USA).gba'

    rombase,ext = os.path.splitext(romname)
    #   'Tiny Toon Adventures - Scary Dreams (USA)'
    match = re.match(regex, rombase)

    # If there's no parentheses in the romname, just use it instead
    basename = match[0].strip() if match != None else rombase.strip()
    return basename

def findCartridgeLabel(romname):
    regex = r"(.*?)(?=\()"
    # At this point, romname is something like 
    #   'Tiny Toon Adventures - Scary Dreams (USA).gba'

    rombase,ext = os.path.splitext(romname)
    #   'Tiny Toon Adventures - Scary Dreams (USA)'
    match = re.match(regex, rombase)

    # If there's no parentheses in the romname, just use it instead
    basename = match[0].strip() if match != None else rombase.strip()

    #   'Tiny Toon Adventures - Scary Dreams'
    for root, dirs, files in os.walk(PACKDIR):
        for name in files:
            if name.lower().startswith(basename.lower()) and os.path.splitext(name)[1][1:].lower() in IMGTYPES:
                return name

    raise Exception("Did not find artwork for %s" % romname)

if __name__ == "__main__":
    backupConfigs()

    csv = ""
    #10yard.zip,mame2014_libretro.dll,1.5,10Yard Splash.dds,HD,LayoutTetris,#000000,#000000,#000000,10Yard Cabinet Normal Front.dds,,10Yard Cabinet Normal Side.dds,,10yard.mp4,,1,No,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
    # FIXME: Use quotes to escape ROMs, labels, Game Titles that have commas
    for dirpath, dirnames, filenames in os.walk(PACKDIR):
        for filename in filenames:
            extension = os.path.splitext(filename)[1][1:]
            if extension in IMGTYPES:
                labelpath = os.path.join(dirpath,filename)
                targetpath = os.path.join(artdir,filename)
                print("Copying label %s to %s" % (labelpath, targetpath))
                shutil.copyfile(labelpath, targetpath)

    for dirpath, dirnames, filenames in os.walk(PACKDIR):
        for filename in filenames:
            extension = os.path.splitext(filename)[1][1:]
            if extension in CORE_DICT.keys():
                romfile = os.path.join(dirpath, filename)
                targetfile = os.path.join(romdir, filename)
                print("Copying romfile %s to %s" % (romfile, targetfile))

                if not DEBUG:
                    shutil.copyfile(romfile, targetfile)
                    
                labelpath = findCartridgeLabel(filename)
                # generate CSV
                # Game,Core,GameName,Texture,Colour,Type,FixedLocation,Include (Yes/No),,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
                # Mega Man 3 (USA).nes,bnes_libretro.dll,Mega Man 3 (NES),Megaman3.dds,#333333,Console,,Yes,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

                # TODO: Cartridge Colors
                gamename = getGameName(filename)
                if "," in filename or "," in gamename or "," in labelpath:
                    raise Exception("Cannot have commas in ROM or artwork name!")
                csvline = ",".join([filename,CORE_DICT[extension],gamename,os.path.split(labelpath)[1],"#333333","Console","","Yes"])
                csv += csvline
                csv += ",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,"
                csv += "\n"

    """
    df = pd.read_csv(csv)
    df.to_csv('output.csv')
    """
    #PACKDIR = "/Users/user/Sync/Streaming/Games/NRAN/Zekupack/ROMs/cartridges"
    
    with open("cartridge_list.csv"),"w") as outfile:
        outfile.write(csv)
    #print(csv)
        
