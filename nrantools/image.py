#!/usr/bin/env python3

import os
import sys
import requests
from urllib.parse import quote
from wand import image
from PIL import Image
from .mame_db import MAMEDatabase

class ImageConverter:
    """Handles image conversion and processing for NRAN content."""
    
    def __init__(self, template_path=None):
        self.template_path = template_path or os.path.join("resources", "art_templates", "FrontTemplate.png")
        self.template_size = 512, 120

    def convert_to_dds(self, imgpath, output_dir):
        """Convert an image to DDS format."""
        with image.Image(filename=imgpath) as img:
            imgfile = os.path.basename(imgpath)
            targetfile = os.path.splitext(imgfile)[0] + ".dds"
            targetpath = os.path.join(output_dir, targetfile)
            print(targetpath)
            img.compression = 'dxt5'
            img.save(filename=targetpath)
            return targetpath

    def create_cabinet_art(self, image_path, output_path="output.png"):
        """Create cabinet art by combining image with template."""
        template = Image.open(self.template_path).convert('RGBA')
        marquee = Image.open(image_path).convert('RGBA')
        
        marquee.thumbnail(self.template_size, Image.Resampling.LANCZOS)
        offset = int((512 - marquee.size[0]) / 2)
        
        # Insert into template image at coordinates 0,51:
        template.paste(marquee, (offset, 51), marquee)
        template.save(output_path)
        return output_path

    def download_marquee_art(self, rom_name, output_dir=".", filename=None):
        """
        Download marquee art from ArcadeItalia for a given ROM name.
        
        Args:
            rom_name (str): The ROM name (without extension)
            output_dir (str): Directory to save the downloaded image
            filename (str): Custom filename (defaults to rom_name.png)
            
        Returns:
            str: Path to the downloaded file, or None if download failed
        """
        # URL encode the ROM name for safe URL construction
        encoded_rom_name = quote(rom_name)
        url = f"https://adb.arcadeitalia.net/media/mame.current/marquees/{encoded_rom_name}.png?release=209"
        
        # Set default filename if not provided
        if not filename:
            filename = f"{rom_name}.png"
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, filename)
        
        try:
            # Download the image
            response = requests.get(url, timeout=30)
            response.raise_for_status()  # Raise exception for HTTP errors
            
            # Check if we actually got image content (not an error page)
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                print(f"Warning: URL did not return image content for {rom_name}")
                return None
            
            # Save the image
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            print(f"Successfully downloaded marquee for {rom_name} to {output_path}")
            return output_path
            
        except requests.exceptions.RequestException as e:
            print(f"Error downloading marquee for {rom_name}: {e}")
            return None
        except IOError as e:
            print(f"Error saving marquee for {rom_name}: {e}")
            return None

    def interactive_marquee_download(self):
        """
        Interactive function that queries user for a game name,
        fuzzy matches against MAME ROM database, and downloads marquee art.
        """
        print("NRAN Tools - Interactive Marquee Downloader")
        print("=" * 50)
        print("This tool helps you find and download marquee artwork for arcade games.")
        print()
        
        # Initialize MAME database
        mame_db = MAMEDatabase()
        
        while True:
            try:
                # Get user input
                query = input("Enter game name or partial ROM name: ").strip()
                
                if not query:
                    print("Please enter a search term.")
                    continue
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                
                print(f"\nSearching for: {query}")
                print("-" * 50)
                
                # Perform fuzzy search
                results = mame_db.fuzzy_search(query, limit=10)
                
                if not results:
                    print("No matches found. Try a different search term.")
                    print()
                    continue
                
                print(f"Found {len(results)} possible matches:")
                print()
                
                # Display results
                for i, (rom_name, rom_info) in enumerate(results, 1):
                    name = rom_info.get('name', 'Unknown')
                    manufacturer = rom_info.get('manufacturer', 'Unknown')
                    year = rom_info.get('year', 'Unknown')
                    
                    print(f"{i:2d}. {rom_name}")
                    print(f"     Title: {name}")
                    print(f"     Manufacturer: {manufacturer}")
                    print(f"     Year: {year}")
                    print()
                
                # Get user selection
                while True:
                    try:
                        selection = input("Enter number to download marquee (or 'back' to search again): ").strip()
                        
                        if selection.lower() in ['back', 'b', '']:
                            break
                        
                        if selection.isdigit():
                            idx = int(selection) - 1
                            if 0 <= idx < len(results):
                                selected_rom = results[idx][0]
                                selected_title = results[idx][1].get('name', selected_rom)
                                
                                print(f"\nDownloading marquee for: {selected_title} ({selected_rom})")
                                
                                # Download the marquee
                                output_dir = "downloaded_marquees"
                                result = self.download_marquee_art(selected_rom, output_dir)
                                
                                if result:
                                    print(f"Successfully downloaded to: {result}")
                                    print(f"File size: {os.path.getsize(result)} bytes")
                                    
                                    # Ask if user wants to convert to DDS
                                    convert_choice = input("Convert to DDS format? (y/n): ").strip().lower()
                                    if convert_choice in ['y', 'yes']:
                                        dds_result = self.convert_to_dds(result, output_dir)
                                        print(f"Converted to DDS: {dds_result}")
                                else:
                                    print(f"Failed to download marquee for: {selected_rom}")
                                
                                print()
                                break
                            else:
                                print("Invalid selection. Please enter a number from the list.")
                        else:
                            print("Please enter a valid number or 'back'.")
                            
                    except ValueError:
                        print("Please enter a valid number or 'back'.")
                
                # Ask if user wants to continue searching
                continue_search = input("Search for another game? (y/n): ").strip().lower()
                if continue_search not in ['y', 'yes']:
                    print("Goodbye!")
                    break
                print()
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
                print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python image.py <input_image> <output_dir>           # Convert to DDS")
        print("  python image.py --download <rom_name> [output_dir] # Download marquee")
        print("  python image.py --interactive                       # Interactive search and download")
        sys.exit(1)
    
    converter = ImageConverter()
    
    if sys.argv[1] == "--download":
        if len(sys.argv) < 3:
            print("Usage: python image.py --download <rom_name> [output_dir]")
            sys.exit(1)
        
        rom_name = sys.argv[2]
        output_dir = sys.argv[3] if len(sys.argv) > 3 else "."
        result = converter.download_marquee_art(rom_name, output_dir)
        
        if result:
            print(f"Downloaded marquee to: {result}")
        else:
            print(f"Failed to download marquee for: {rom_name}")
    elif sys.argv[1] == "--interactive":
        converter.interactive_marquee_download()
    else:
        # Original DDS conversion functionality
        if len(sys.argv) != 3:
            print("Usage: python image.py <input_image> <output_dir>")
            sys.exit(1)
        
        converter.convert_to_dds(sys.argv[1], sys.argv[2])
