#!/usr/bin/env python3

import os
import sys
import shutil
import re

# FIXME get this from environment?

#NRAN_CONTENT_DIR = os.getenv("NRAN_CONTENT_DIR")
NRAN_CONTENT_DIR = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\New Retro Arcade Neon\\NewRetroArcade\\Content"
os.getenv("NRAN_CONTENT_DIR")

NRAN_ROMDIR = os.path.join(NRAN_CONTENT_DIR, "Roms")
NRAN_ARTDIR = os.path.join(NRAN_CONTENT_DIR, "Cartridges")

#PACKDIR = "/Users/user/Sync/Streaming/Games/NRAN/Zekupack/ROMs/cartridges"
PACKDIR = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\New Retro Arcade Neon\\NewRetroArcade"

NES_CORE = "bnes_libretro" 
SNES_CORE = "bsnes_performance_libretro.dll" 
GEN_CORE = "picodrive_libretro.dll"
GBA_CORE = "mgba_libretro.dll"

ROMTYPES = ["smc","sfc","gba", "md","nes"]
IMAGETYPES = ["png","dds"]

def findCartridgeLabel(romname):
    regex = r"(.*?)(?=\()"
    # At this point, romname is something like 
    #   'Tiny Toon Adventures - Scary Dreams (USA).gba'

    rombase,ext = os.path.splitext(romname)
    #   'Tiny Toon Adventures - Scary Dreams (USA)'
    match = re.match(regex, rombase)
    basename = match[0].strip() if match != None else rombase.strip()
    print(basename)
    #   'Tiny Toon Adventures - Scary Dreams'
    import code
    #code.interact(local=locals())

if __name__ == "__main__":
    # Copy all subdirectories in
    for dirpath, dirnames, filenames in os.walk(PACKDIR):
        for filename in filenames:
            if os.path.splitext(filename)[1][1:] in ROMTYPES:
                romfile = os.path.join(dirpath,filename)
                findCartridgeLabel(filename)

                # TODO actually copy it
                #shutil.copyfile(romfile,

#supermarioworld.smc,bsnes_performance_libretro.dll,Super Mario World,snes_mario.dds,#FFFFFF,Console,,Yes
