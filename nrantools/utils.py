#!/usr/bin/env python3

import os
import pandas as pd
from .mame_db import MAMEDatabase

class Utils:
    """Utility functions for NRAN content management."""
    
    @staticmethod
    def remove_duplicates(csv_path, output_path="output.csv"):
        """Remove duplicate entries from a CSV file."""
        df = pd.read_csv(csv_path)
        df = df.drop_duplicates(keep='first')
        df.to_csv(output_path, index=False)
        return output_path

    @staticmethod
    def find_missing_roms(csv_path, roms_dir):
        """Find ROMs that don't have entries in the CSV file."""
        if os.path.exists(csv_path):
            cabinets = open(csv_path).read()
        else:
            cabinets = ""
        
        missing_roms = []
        for dirpath, dirnames, filenames in os.walk(roms_dir):
            for name in filenames:
                if name not in cabinets:
                    missing_roms.append(name)
        
        return missing_roms

    @staticmethod
    def fuzzy_search(query, limit=5):
        """
        Perform fuzzy search against MAME ROM database and print results.
        
        Args:
            query (str): Search string
            limit (int): Maximum number of results to return
            
        Returns:
            List of tuples (rom_name, rom_info) sorted by similarity
        """
        db = MAMEDatabase()
        
        print(f"Search: '{query}'")
        print("-" * 30)
        
        results = db.fuzzy_search(query, limit=limit)
        
        if results:
            for i, (rom_name, rom_info) in enumerate(results, 1):
                name = rom_info.get('name', 'Unknown')
                manufacturer = rom_info.get('manufacturer', 'Unknown')
                year = rom_info.get('year', 'Unknown')
                
                print(f"{i}. {rom_name}")
                print(f"   Title: {name}")
                print(f"   Manufacturer: {manufacturer}")
                print(f"   Year: {year}")
        else:
            print("No matches found")
        
        return results

if __name__ == "__main__":
    # Example usage
    utils = Utils()
    # utils.remove_duplicates("cartridge_list.csv")
    # missing = utils.find_missing_roms("cabinet_list.csv", "roms_directory")
    # print("Missing ROMs:", missing)
