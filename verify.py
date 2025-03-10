import os
import shutil
from tempfile import TemporaryDirectory

from wand import image

# TODO: Do we even need this? ArcadeManager doesn't seem to convert at all
import dds

# New Retro Arcade:Neon Content directory
CONTENT_DIRECTORY = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\New Retro Arcade Neon\\NewRetroArcade\\Content"
CSV_FIRSTLINE = "Game,Core,GameName,Texture,Colour,Type,FixedLocation,Include (Yes/No),,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,"

# Make sure it's the right directory
# FIXME I don't think we need this anymore
"""
assert os.path.exists(os.path.join(BASE_DIRECTORY,"ArcadeCartridges.xml"))
assert os.path.exists(os.path.join(BASE_DIRECTORY,"ArcadeMachines.xml"))
assert os.path.exists(os.path.join(BASE_DIRECTORY,"ArcadeMusic.xml"))
assert os.path.exists(os.path.join(BASE_DIRECTORY,"ArcadePosters.xml"))
"""

# TODO: move config to separate file
NES_COLOR = "#525151"
SNES_COLOR = "#E5E5E5"
GENESIS_COLOR = "#000000"

NES_CORE = "bnes_retrocore.dll"
SNES_CORE = "bsnes_performance_libretro.dll"
MD_CORE = "picodrive_libretro.dll"


OUTPUT_DIRECTORY = "Content"
CART_DIRECTORY = os.path.join(OUTPUT_DIRECTORY, "Cartridges")

if not os.path.exists(OUTPUT_DIRECTORY):
    os.mkdir(OUTPUT_DIRECTORY)
if not os.path.exists(CART_DIRECTORY):
    os.mkdir(CART_DIRECTORY)


ROMTYPES = ['nes','smc','sfc','md','gen','gb','gbc','gba']
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

                    # We found it
                    if len(maybe_coverart) == 2:
                        # The list should contain the rom and the art, remove the rom
                        maybe_coverart.remove(f)
                        # Game,Core,GameName,Texture,Colour,Type,FixedLocation,Include (Yes/No),,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
                        # Mega Man 2 (USA).nes,bnes_libretro.dll,Mega Man 2 (NES),output.dds,#333333,Console,CartridgeTable1,Yes,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
                        l = []
                        line = ""
                        """
                        if "," in f:
                            # FIXME we may be able to just put it in quotes?
                            raise Exception("There is a game name with comma! This will screw things up, please rename %s" % f)
                        """

                        if f.endswith(".nes"):
                            core = NES_CORE
                            color = NES_COLOR

                        elif f.endswith(".smc") or f.endswith(".sfc"):
                            pass

                        elif f.endswith(".md") or f.endswith(".gen"):
                            pass

                        else:
                            raise UnsupportedOperationException("Error processing %s" % f)
                        l = ["\"" + f +"\"", core, name, "\"" + maybe_coverart[0]+"\"",color,"#1F1F1F","","","Yes"]
                        line = ','.join(l)+",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n"
                        csv += line


                        # Copy ROM
                        src = os.path.join(root,f)
                        dest = os.path.join(CART_DIRECTORY,f)
                        shutil.copyfile(src, dest)

                        # Copy Coverart
                        src = os.path.join(root,maybe_coverart[0])
                        dest = os.path.join(CART_DIRECTORY,maybe_coverart[0])
                        shutil.copyfile(src, dest)


                        import code
                        #code.interact(local=locals())

                        break

                        #print("%s:%s" % (f, maybe_coverart[0]))

    return csv

if __name__ == "__main__":
    cartridge_xml = ""
    cartridge_xml += checkCartDirectory(os.path.join("..","NES"))
    #r = checkCartDirectory(os.path.join("..","SNES"))
    with open("cartridge_list.csv",'w') as cartfile:
        cartfile.write(cartridge_xml)
    
