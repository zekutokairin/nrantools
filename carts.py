#!/usr/bin/env python3

import os
import sys
import shutil
import re

DEBUG = os.getenv("NRAN_DEBUG")

#NRAN_CONTENT_DIR = os.getenv("NRAN_CONTENT_DIR")
NRAN_CONTENT_DIR = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\New Retro Arcade Neon\\NewRetroArcade\\Content"
os.getenv("NRAN_CONTENT_DIR")

NRAN_ROMDIR = os.path.join(NRAN_CONTENT_DIR, "Roms")
NRAN_ARTDIR = os.path.join(NRAN_CONTENT_DIR, "Cartridges")

#PACKDIR = "/Users/user/Sync/Streaming/Games/NRAN/Zekupack/ROMs/cartridges"
#PACKDIR = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\New Retro Arcade Neon\\NewRetroArcade"
PACKDIR = "D:\\Streaming\\Games\\NRAN\\Zekupack"
CARTDIR = "D:\\Streaming\\Games\\NRAN\\Zekupack"

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
    for root, dirs, files in os.walk(NRAN_ARTDIR):
        for name in files:
            if name.lower().startswith(basename.lower()) and os.path.splitext(name)[1][1:].lower() in IMGTYPES:
                return name

    raise Exception("Did not find artwork for %s" % romname)

if __name__ == "__main__":
    # Copy all subdirectories in

    csv = ""
    #10yard.zip,mame2014_libretro.dll,1.5,10Yard Splash.dds,HD,LayoutTetris,#000000,#000000,#000000,10Yard Cabinet Normal Front.dds,,10Yard Cabinet Normal Side.dds,,10yard.mp4,,1,No,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
    for dirpath, dirnames, filenames in os.walk(PACKDIR):
        for filename in filenames:
            extension = os.path.splitext(filename)[1][1:]
            if extension in IMGTYPES:
                labelpath = os.path.join(dirpath,filename)
                print("Copying label %s to %s" % (labelpath, NRAN_ARTDIR))
                shutil.copyfile(labelpath, NRAN_ARTDIR)

    for dirpath, dirnames, filenames in os.walk(PACKDIR):
        for filename in filenames:
            extension = os.path.splitext(filename)[1][1:]
            if extension in CORE_DICT.keys():
                romfile = os.path.join(dirpath,filename)
                print("Copying romfile %s to %s" % (romfile, NRAN_ROMDIR))

                if not DEBUG:
                    shutil.copyfile(romfile, NRAN_ROMDIR)
                    
                labelpath = findCartridgeLabel(filename)
                # generate CSV
                # Game,Core,GameName,Texture,Colour,Type,FixedLocation,Include (Yes/No),,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
                # Mega Man 3 (USA).nes,bnes_libretro.dll,Mega Man 3 (NES),Megaman3.dds,#333333,Console,,Yes,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
                # D:\Streaming\Games\NRAN\Zekupack\ROMs\cartridges\SNES\Super Star Wars (USA) (Rev 1).sfc,bsnes_performance_libretro.dll,Super Star Wars,super_star_wars_usa_rev_1.dds,#333333,Console,,Yes,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

                # TODO: Cartridge Colors
                csvline = ",".join([romfile,CORE_DICT[extension],"SomeGame",labelpath,"#333333","Console","","Yes"])
                #print(csvline)
                csv += csvline + "\n"

    # TODO: Read the existing cartridge CSV and add our new stuff at the end
    print(csv)
