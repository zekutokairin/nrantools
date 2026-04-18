#!/usr/bin/env python3

import os
import shutil
from tempfile import TemporaryDirectory

class ContentVerifier:
    """Verifies and validates NRAN content directories and files."""
    
    def __init__(self, content_directory=None, output_directory="Content"):
        self.CONTENT_DIRECTORY = content_directory or "C:\\Program Files (x86)\\Steam\\steamapps\\common\\New Retro Arcade Neon\\NewRetroArcade\\Content"
        self.OUTPUT_DIRECTORY = output_directory
        self.CART_DIRECTORY = os.path.join(output_directory, "Cartridges")
        
        # CSV header for cartridge list
        self.CSV_FIRSTLINE = "Game,Core,GameName,Texture,Colour,Type,FixedLocation,Include (Yes/No),,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,"
        
        # ROM and image types
        self.ROMTYPES = ['nes', 'smc', 'sfc', 'md', 'gen', 'gb', 'gbc', 'gba']
        self.IMAGETYPES = ['png', 'gif', 'jpg']
        
        # Core mappings
        self.NES_CORE = "bnes_retrocore.dll"
        self.SNES_CORE = "bsnes_performance_libretro.dll"
        self.MD_CORE = "picodrive_libretro.dll"
        
        # Color mappings
        self.NES_COLOR = "#525151"
        self.SNES_COLOR = "#E5E5E5"
        self.MD_COLOR = "#000000"
        
        # Create output directories if they don't exist
        if not os.path.exists(self.OUTPUT_DIRECTORY):
            os.mkdir(self.OUTPUT_DIRECTORY)
        if not os.path.exists(self.CART_DIRECTORY):
            os.mkdir(self.CART_DIRECTORY)
        
        # List of ROM objects
        self.ROMS = []

    class ROM:
        def __init__(self, Game, Core, GameName, Texture, Colour):
            self.Game = Game
            self.Core = Core
            self.GameName = GameName
            self.Texture = Texture
            self.Colour = Colour

    def check_cart_directory(self, path):
        """Check a directory of ROMs/artwork and return CSV for NRAN Arcade Manager."""
        cart_dict = {}
        csv = self.CSV_FIRSTLINE + "\n"
        
        for root, dirs, files in os.walk(path):
            for f in files:
                name, ext = os.path.splitext(f)

                # It is a ROM
                if ext[1:].lower() in self.ROMTYPES:
                    # Search the directory for a cover file
                    coverart = None
                    for i in range(len(name), 1, -1):
                        # Get all files starting with the same name
                        maybe_coverart = [x for x in files if os.path.splitext(x)[0].startswith(name[0:i])]

                        # We didn't find anything, try again with a shorter version
                        if len(maybe_coverart) == 0:
                            continue

                        # We found it - the list should contain the rom and the art, remove the rom
                        if len(maybe_coverart) == 2:
                            maybe_coverart.remove(f)

                            # Determine core and color based on file extension
                            if f.endswith(".nes"):
                                core = self.NES_CORE
                                color = self.NES_COLOR
                            elif f.endswith(".smc") or f.endswith(".sfc"):
                                core = self.SNES_CORE
                                color = self.SNES_COLOR
                            elif f.endswith(".md") or f.endswith(".gen"):
                                core = self.MD_CORE
                                color = self.MD_COLOR
                            else:
                                raise Exception("Unsupported ROM type: %s" % f)

                            # Create CSV line
                            line_items = ['"' + f + '"', core, '"' + name + '"', '"' + maybe_coverart[0] + '"', 
                                        color, "Console", "", "Yes"]
                            line = ','.join(line_items) + "\n"
                            csv += line

                            # Copy ROM
                            src = os.path.join(root, f)
                            dest = os.path.join(self.CART_DIRECTORY, f)
                            shutil.copyfile(src, dest)

                            # Copy Coverart
                            src = os.path.join(root, maybe_coverart[0])
                            dest = os.path.join(self.CART_DIRECTORY, maybe_coverart[0])
                            shutil.copyfile(src, dest)

                            # Add to ROMS list
                            game = self.ROM(Game=f, Core=core, GameName=name, 
                                         Texture=maybe_coverart[0], Colour=color)
                            self.ROMS.append(game)

                            break

        return csv

    def verify_content(self, path):
        """Verify content in the given path and return validation results."""
        csv_data = self.check_cart_directory(path)
        return csv_data

if __name__ == "__main__":
    verifier = ContentVerifier()
    cartridge_xml = verifier.check_cart_directory(os.path.join("..", "NES"))
    
    with open("cartridge_list.csv", 'w') as cartfile:
        cartfile.write(cartridge_xml)
