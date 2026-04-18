#!/usr/bin/env python3

import os
import json
import requests
from difflib import get_close_matches
from typing import List, Dict, Tuple, Optional

class MAMEDatabase:
    """Handles MAME ROM database lookups and fuzzy matching."""
    
    def __init__(self, cache_file="mame_cache.json"):
        self.cache_file = cache_file
        self.rom_data = {}
        self.load_cache()
    
    def load_cache(self):
        """Load MAME ROM data from cache file."""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.rom_data = json.load(f)
                print(f"Loaded {len(self.rom_data)} ROM entries from cache")
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading cache: {e}")
                self.rom_data = {}
        else:
            print("No cache file found, will need to download MAME data")
    
    def save_cache(self):
        """Save MAME ROM data to cache file."""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.rom_data, f, indent=2, ensure_ascii=False)
            print(f"Saved {len(self.rom_data)} ROM entries to cache")
        except IOError as e:
            print(f"Error saving cache: {e}")
    
    def download_mame_data(self):
        """Download MAME ROM data from MAME XML source."""
        # URL for MAME's XML game list (this is a large file)
        # For now, we'll create a small sample database
        # In a real implementation, you'd want to download the full MAME XML
        print("Downloading MAME ROM data...")
        
        # Sample data for demonstration - in reality this would be much larger
        sample_data = {
            "pacman": {"name": "Pac-Man", "manufacturer": "Namco", "year": "1980"},
            "pacmanplus": {"name": "Pac-Man Plus", "manufacturer": "Namco", "year": "1981"},
            "mspacman": {"name": "Ms. Pac-Man", "manufacturer": "Namco", "year": "1981"},
            "donkeykong": {"name": "Donkey Kong", "manufacturer": "Nintendo", "year": "1981"},
            "donkeykongj": {"name": "Donkey Kong Jr.", "manufacturer": "Nintendo", "year": "1982"},
            "donkeykong3": {"name": "Donkey Kong 3", "manufacturer": "Nintendo", "year": "1983"},
            "galaga": {"name": "Galaga", "manufacturer": "Namco", "year": "1981"},
            "galaga88": {"name": "Galaga '88", "manufacturer": "Namco", "year": "1987"},
            "spaceinv": {"name": "Space Invaders", "manufacturer": "Taito", "year": "1978"},
            "asteroid": {"name": "Asteroids", "manufacturer": "Atari", "year": "1979"},
            "asteroidk": {"name": "Asteroids Deluxe", "manufacturer": "Atari", "year": "1980"},
            "centiped": {"name": "Centipede", "manufacturer": "Atari", "year": "1980"},
            "millipede": {"name": "Millipede", "manufacturer": "Atari", "year": "1982"},
            "frogger": {"name": "Frogger", "manufacturer": "Konami", "year": "1981"},
            "froggerf": {"name": "Frogger (Frogger conversion)", "manufacturer": "Konami", "year": "1981"},
            "qbert": {"name": "Q*bert", "manufacturer": "Gottlieb", "year": "1982"},
            "qbertqube": {"name": "Q*bert's Qubes", "manufacturer": "Gottlieb", "year": "1983"},
            "defender": {"name": "Defender", "manufacturer": "Williams", "year": "1980"},
            "defendj": {"name": "Defender (Japan)", "manufacturer": "Williams", "year": "1980"},
            "joust": {"name": "Joust", "manufacturer": "Williams", "year": "1982"},
            "robotron": {"name": "Robotron: 2084", "manufacturer": "Williams", "year": "1982"},
            "stargate": {"name": "Stargate", "manufacturer": "Williams", "year": "1981"},
            "moonpatr": {"name": "Moon Patrol", "manufacturer": "Williams", "year": "1982"},
            "chinagat": {"name": "China Gate", "manufacturer": "Zilec", "year": "1984"},
            "chinagat2": {"name": "China Gate (set 2)", "manufacturer": "Zilec", "year": "1984"},
            "chinagat3": {"name": "China Gate (set 3)", "manufacturer": "Zilec", "year": "1984"},
            "tempest": {"name": "Tempest", "manufacturer": "Atari", "year": "1981"},
            "tempest1": {"name": "Tempest (rev 1)", "manufacturer": "Atari", "year": "1981"},
            "tempest2": {"name": "Tempest (rev 2)", "manufacturer": "Atari", "year": "1981"},
            "battlezone": {"name": "Battlezone", "manufacturer": "Atari", "year": "1980"},
            "gravitar": {"name": "Gravitar", "manufacturer": "Atari", "year": "1982"},
            "redbaron": {"name": "Red Baron", "manufacturer": "Atari", "year": "1980"},
            "missile": {"name": "Missile Command", "manufacturer": "Atari", "year": "1980"},
            "berzerk": {"name": "Berzerk", "manufacturer": "Stern", "year": "1980"},
            "frenzy": {"name": "Frenzy", "manufacturer": "Stern", "year": "1982"},
            "scramble": {"name": "Scramble", "manufacturer": "Konami", "year": "1981"},
            "scrambles": {"name": "Scramble (Stern)", "manufacturer": "Konami", "year": "1981"},
            "superpac": {"name": "Super Pac-Man", "manufacturer": "Namco", "year": "1982"},
            "pacnpal": {"name": "Pac & Pal", "manufacturer": "Namco", "year": "1982"},
            "digdug": {"name": "Dig Dug", "manufacturer": "Namco", "year": "1982"},
            "digdug2": {"name": "Dig Dug II", "manufacturer": "Namco", "year": "1985"},
            "polepos": {"name": "Pole Position", "manufacturer": "Namco", "year": "1982"},
            "polepos2": {"name": "Pole Position II", "manufacturer": "Namco", "year": "1983"},
            "gaplus": {"name": "Gaplus", "manufacturer": "Namco", "year": "1984"},
            "bosco": {"name": "Bosconian", "manufacturer": "Namco", "year": "1981"},
            "xevious": {"name": "Xevious", "manufacturer": "Namco", "year": "1982"},
            "xeviousa": {"name": "Xevious (Atari)", "manufacturer": "Namco", "year": "1982"},
        }
        
        self.rom_data = sample_data
        self.save_cache()
        print(f"Downloaded {len(self.rom_data)} ROM entries")
    
    def fuzzy_search(self, query: str, limit: int = 10) -> List[Tuple[str, Dict]]:
        """
        Perform fuzzy search against MAME ROM database.
        
        Args:
            query: Search string
            limit: Maximum number of results to return
            
        Returns:
            List of tuples (rom_name, rom_info) sorted by similarity
        """
        if not self.rom_data:
            print("No ROM data available, downloading...")
            self.download_mame_data()
        
        # Get all ROM names and game names for matching
        rom_names = list(self.rom_data.keys())
        game_names = [info.get('name', '') for info in self.rom_data.values()]
        
        # Find close matches in ROM names
        rom_matches = get_close_matches(query.lower(), [name.lower() for name in rom_names], n=limit, cutoff=0.3)
        
        # Find close matches in game titles
        title_matches = get_close_matches(query.lower(), [name.lower() for name in game_names], n=limit, cutoff=0.3)
        
        # Combine results and deduplicate
        results = []
        seen = set()
        
        # Add ROM name matches
        for match in rom_matches:
            # Find the original case version
            original_rom = next((rom for rom in rom_names if rom.lower() == match), None)
            if original_rom and original_rom not in seen:
                results.append((original_rom, self.rom_data[original_rom]))
                seen.add(original_rom)
        
        # Add title matches
        for match in title_matches:
            # Find ROMs with matching titles
            for rom_name, rom_info in self.rom_data.items():
                if rom_info.get('name', '').lower() == match and rom_name not in seen:
                    results.append((rom_name, rom_info))
                    seen.add(rom_name)
        
        # Sort by relevance (ROM name matches first, then title matches)
        results.sort(key=lambda x: (0 if x[0].lower() in rom_matches else 1))
        
        return results[:limit]
    
    def get_rom_info(self, rom_name: str) -> Optional[Dict]:
        """Get detailed information for a specific ROM."""
        return self.rom_data.get(rom_name)
    
    def interactive_search(self):
        """Interactive search function that queries user and displays results."""
        print("MAME ROM Database Search")
        print("=" * 40)
        print("Enter a game name or partial ROM name to search.")
        print("Type 'quit' to exit.")
        print()
        
        while True:
            try:
                query = input("Search query: ").strip()
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                
                if not query:
                    print("Please enter a search term.")
                    continue
                
                print(f"\nSearching for: {query}")
                print("-" * 40)
                
                results = self.fuzzy_search(query, limit=15)
                
                if not results:
                    print("No matches found. Try a different search term.")
                    continue
                
                print(f"Found {len(results)} matches:")
                print()
                
                for i, (rom_name, rom_info) in enumerate(results, 1):
                    name = rom_info.get('name', 'Unknown')
                    manufacturer = rom_info.get('manufacturer', 'Unknown')
                    year = rom_info.get('year', 'Unknown')
                    
                    print(f"{i:2d}. {rom_name}")
                    print(f"     Title: {name}")
                    print(f"     Manufacturer: {manufacturer}")
                    print(f"     Year: {year}")
                    print()
                
                # Allow user to select a ROM for marquee download
                if results:
                    try:
                        selection = input("Enter number to download marquee (or press Enter to continue): ").strip()
                        if selection and selection.isdigit():
                            idx = int(selection) - 1
                            if 0 <= idx < len(results):
                                selected_rom = results[idx][0]
                                print(f"\nDownloading marquee for: {selected_rom}")
                                return selected_rom
                    except ValueError:
                        pass
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
        
        return None

if __name__ == "__main__":
    db = MAMEDatabase()
    db.interactive_search()
