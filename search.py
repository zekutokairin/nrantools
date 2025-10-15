#!/usr/bin/env python3
import os
import sys

CSVPATH = os.path.join("tests","csv","cabinet_list.csv")
cabinets = open(CSVPATH).read()

if __name__ == "__main__":
    romdir = sys.argv[1]
    # Scan ROMs folder
    # TODO: Rename to canonical (no-intro) names based on hash
    # Print the roms that do not have entries in the CSV
    for dirpath, dirnames, filenames in os.walk(romdir):
        for name in filenames:
            if name not in cabinets:
                print(name)

#print(cabinets)