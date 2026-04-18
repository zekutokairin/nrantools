#!/usr/bin/env python3

import os
import sys
import datetime
import shutil
import re
import pandas as pd

class CartridgeManager:
    """Manages ROM cartridges and artwork for New Retro Arcade:Neon."""
    
    def __init__(self, pack_dir=None, content_dir=None, output_dir="output"):
        self.DEBUG = os.getenv("NRAN_DEBUG")
        
        # Default content directory for NRAN
        self.NRAN_CONTENT_DIR = content_dir or "C:\\Program Files (x86)\\Steam\\steamapps\\common\\New Retro Arcade Neon\\NewRetroArcade\\Content"
        
        # Pack directory where ROMs and artwork are stored
        self.PACKDIR = pack_dir or os.getenv("NRAN_PACK")
        if not self.PACKDIR:
            raise Exception("Need to define NRAN_PACK environment variable with your pack directory!")
        
        # Output directories
        self.outputdir = output_dir
        self.romdir = os.path.join(output_dir, "Roms")
        self.artdir = os.path.join(output_dir, "Cartridges")
        self.backupdir = os.path.join(output_dir, "backups")
        
        # Create directories if they don't exist
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(self.romdir, exist_ok=True)
        os.makedirs(self.artdir, exist_ok=True)
        os.makedirs(self.backupdir, exist_ok=True)
        
        # Core mappings for different ROM types
        self.NES_CORE = "bnes_libretro.dll" 
        self.SNES_CORE = "bsnes_performance_libretro.dll" 
        self.GEN_CORE = "picodrive_libretro.dll"
        self.GBA_CORE = "mgba_libretro.dll"
        
        self.CORE_DICT = {
            "smc": self.SNES_CORE,
            "sfc": self.SNES_CORE,
            "nes": self.NES_CORE,
            "gg": self.GEN_CORE,
            "gba": self.GBA_CORE,
            "md": self.GEN_CORE
        }
        
        self.IMGTYPES = ["jpg", "jpeg", "png", "dds"]

    def backup_configs(self):
        """Backup NRAN configuration files."""
        d = datetime.datetime.now()
        timestamp = "%04d%02d%02d_%02d%02d" % (d.year, d.month, d.day, d.hour, d.minute) 
        currentbackup = os.path.join(self.backupdir, timestamp)

        os.makedirs(self.backupdir, exist_ok=True)
        os.makedirs(currentbackup, exist_ok=True)

        for f in os.listdir(self.NRAN_CONTENT_DIR):
            extension = os.path.splitext(f)[1].lower()[1:]
            if extension in ["ini", "xml", "csv"]:
                shutil.copyfile(os.path.join(self.NRAN_CONTENT_DIR, f), os.path.join(currentbackup, f))

    def get_game_name(self, romname):
        """Extract clean game name from ROM filename."""
        regex = r"(.*?)(?=\()"
        rombase, ext = os.path.splitext(romname)
        match = re.match(regex, rombase)
        
        # If there's no parentheses in the romname, just use it instead
        basename = match[0].strip() if match != None else rombase.strip()
        return basename

    def find_cartridge_label(self, romname):
        """Find cartridge artwork for a given ROM."""
        regex = r"(.*?)(?=\()"
        rombase, ext = os.path.splitext(romname)
        match = re.match(regex, rombase)
        
        # If there's no parentheses in the romname, just use it instead
        basename = match[0].strip() if match != None else rombase.strip()

        for root, dirs, files in os.walk(self.PACKDIR):
            for name in files:
                if name.lower().startswith(basename.lower()) and os.path.splitext(name)[1][1:].lower() in self.IMGTYPES:
                    return name

        raise Exception("Did not find artwork for %s" % romname)

    def process_cartridges(self):
        """Process all ROMs and artwork to create cartridge pack."""
        self.backup_configs()
        
        csv = ""
        
        # Copy artwork files
        for dirpath, dirnames, filenames in os.walk(self.PACKDIR):
            for filename in filenames:
                extension = os.path.splitext(filename)[1][1:]
                if extension in self.IMGTYPES:
                    labelpath = os.path.join(dirpath, filename)
                    targetpath = os.path.join(self.artdir, filename)
                    print("Copying label %s to %s" % (labelpath, targetpath))
                    shutil.copyfile(labelpath, targetpath)

        # Process ROM files
        for dirpath, dirnames, filenames in os.walk(self.PACKDIR):
            for filename in filenames:
                extension = os.path.splitext(filename)[1][1:]
                if extension in self.CORE_DICT.keys():
                    romfile = os.path.join(dirpath, filename)
                    targetfile = os.path.join(self.romdir, filename)
                    print("Copying romfile %s to %s" % (romfile, targetfile))

                    if not self.DEBUG:
                        shutil.copyfile(romfile, targetfile)
                        
                    labelpath = self.find_cartridge_label(filename)
                    gamename = self.get_game_name(filename)
                    
                    if "," in filename or "," in gamename or "," in labelpath:
                        raise Exception("Cannot have commas in ROM or artwork name!")
                    
                    csvline = ",".join([filename, self.CORE_DICT[extension], gamename, 
                                      os.path.split(labelpath)[1], "#333333", "Console", "", "Yes"])
                    csv += csvline
                    csv += ",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,"
                    csv += "\n"
        
        # Write CSV file
        with open("cartridge_list.csv", "w") as outfile:
            outfile.write(csv)

if __name__ == "__main__":
    manager = CartridgeManager()
    manager.process_cartridges()
