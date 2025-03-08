import os
import shutil
from tempfile import TemporaryDirectory

from wand import image

# New Retro Arcade:Neon Content directory
BASE_DIRECTORY = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\New Retro Arcade Neon\\NewRetroArcade\\Content"
CSV_FIRSTLINE = "Game,Core,GameName,Texture,Colour,Type,FixedLocation,Include (Yes/No),,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,"

# Make sure it's the right directory
assert os.path.exists(os.path.join(BASE_DIRECTORY,"ArcadeCartridges.xml"))
assert os.path.exists(os.path.join(BASE_DIRECTORY,"ArcadeMachines.xml"))
assert os.path.exists(os.path.join(BASE_DIRECTORY,"ArcadeMusic.xml"))
assert os.path.exists(os.path.join(BASE_DIRECTORY,"ArcadePosters.xml"))

NES_COLOR = "#525151"
SNES_COLOR = "#E5E5E5"
GENESIS_COLOR = "#000000"

# TODO: Create if doesn't exist
OUTPUT_DIRECTORY = "output"

ROMTYPES = ['nes','smc','sfc','md','gb','gbc','gba']
IMAGETYPES = ['png','gif','jpg']

def checkCartDirectory(path):
    cart_dict = {}
    csv = CSV_FIRSTLINE + "\n"
    # Given a directory of ROMs/artwork:
    # 1) Verify that every ROM has artwork
    # 2) Return a CSV string for the NRAN Arcade Manager
    for root, dirs, files in os.walk(path):
        for f in files:
            name, ext = os.path.splitext(f)

            # It is a ROM
            if ext[1:].lower() in ROMTYPES:
                # Search the directory for a cover file
                coverart = None
                for i in range(len(name),1, -1):
                    # Get all files starting with the same name
                    maybe_coverart = [x for x in files if os.path.splitext(x)[0].startswith(name[0:i])]

                    # We didn't find anything, try again with a shorter version of
                    # the filename
                    if len(maybe_coverart) == 0:
                        continue

                    if len(maybe_coverart) == 2:
                        # The list should contain the rom and the art, remove the rom
                        maybe_coverart.remove(f)
                        #Game,Core,GameName,Texture,Colour,Type,FixedLocation,Include (Yes/No),,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
                        # Mega Man 2 (USA).nes,bnes_libretro.dll,Mega Man 2 (NES),output.dds,#333333,Console,CartridgeTable1,Yes,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
                        l = []
                        line = ""
                        if f.endswith(".nes"):
                            l = [f, "bsnes_retrocore.dll", name, maybe_coverart[0],"#1F1F1F","","","Yes"] 
                            line = ','.join(l)+",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,"
                            print(line)
                        csv += line
                        csv += "\n"

                        #print("%s:%s" % (f, maybe_coverart[0]))
                        break

    return csv

def ytBacklog():
    # get user playlist public/unlinked
    # return list of urls to write into CSV
    pass

if __name__ == "__main__":
    cartridge_xml = CSV_FIRSTLINE + "\n"
    # TODO: Create --delete option that deletes Carts, Tapes, and Posters not
    #       in the user's content directory
    cartridge_xml += checkCartDirectory(os.path.join("..","NES"))
    #r = checkCartDirectory(os.path.join("..","SNES"))
    with open("ArcadeCartridges.xml",'w') as cartfile:
        cartfile.write(cartridge_xml)
    
