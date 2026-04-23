#!/usr/bin/env python3

import os
import sys
import requests
from urllib.parse import quote
from wand import image
from PIL import Image, ImageOps
from .mame_db import MAMEDatabase

class ImageConverter:
    """Handles image conversion and processing for NRAN content."""
    
    def __init__(self, template_path=None):
        self.template_path = template_path or os.path.join("resources", "art_templates", "FrontTemplate.png")
        self.side_art_template_path = os.path.join("resources", "art_templates", "SideTemplate.png")
        self.template_size = 512, 120
        
        # Get NRAN_PACK environment variable for base directory
        self.nran_pack = os.getenv("NRAN_PACK")
        if not self.nran_pack:
            raise Exception("Need to define NRAN_PACK environment variable with your pack directory!")
        
        # Create content subdirectories
        # Art to go on the top of the cabinet display, the marquee
        self.marquee_dir = os.path.join(self.nran_pack, "marquees")
        # Art to go on the sides of a cabinet
        self.decals_dir = os.path.join(self.nran_pack, "decals")
        # The title screen
        self.titles_dir = os.path.join(self.nran_pack, "titles")
        # The finished artwork texture to go into the Arcades directory in Content
        self.cabinet_art_dir = os.path.join(self.nran_pack, "Arcades")
        
        # Ensure directories exist
        os.makedirs(self.marquee_dir, exist_ok=True)
        os.makedirs(self.decals_dir, exist_ok=True)
        os.makedirs(self.titles_dir, exist_ok=True)
        os.makedirs(self.cabinet_art_dir, exist_ok=True)
        os.makedirs(self.dds_dir, exist_ok=True)

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

        # Create front art
        template = Image.open(self.template_path).convert('RGBA')
        marquee = Image.open(image_path).convert('RGBA')
        
        marquee = ImageOps.fit(marquee, self.template_size, Image.Resampling.LANCZOS, centering=(0.5, 0.5))
        #marquee.thumbnail(self.template_size, Image.Resampling.LANCZOS)
        offset = int((512 - marquee.size[0]) / 2)
        
        # Insert into template image at coordinates 0,51:
        template.paste(marquee, (offset, 51), marquee)
        template.save(output_path)
        return output_path

    def create_side_art(self, image_path, output_path="output.png"):
        # Create side art
        max_size = (260, 410)
        template = Image.open(self.side_art_template_path).convert('RGBA')
        decal = Image.open(image_path).convert('RGBA')
        
        # Resize decal to at most 260x410   
        decal.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Insert left decal into template image 
        template.paste(decal, (150, 300), decal)
        # Insert right decal into template image 
        template.paste(decal, (450, 300), decal)
        template.save(output_path)
        return output_path

    def _download_image(self, url, output_path, rom_name, image_type="image"):
        """
        Helper method to download an image with graceful error handling.
        
        Args:
            url: URL to download from
            output_path: Path to save the file
            rom_name: ROM name for logging
            image_type: Type of image for logging (marquee/decal)
            
        Returns:
            str: Path to downloaded file, or None if download failed
        """
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Check if we actually got image content
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                print(f"Warning: URL did not return image content for {rom_name}")
                return None
            
            # Save the image
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            print(f"Successfully downloaded {image_type} for {rom_name} to {output_path}")
            return output_path
            
        except requests.exceptions.HTTPError as e:
            # Gracefully handle 404 errors
            if e.response.status_code == 404:
                print(f"No {image_type} available for {rom_name} (404)")
            else:
                print(f"HTTP error downloading {image_type} for {rom_name}: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {image_type} for {rom_name}: {e}")
            return None
        except IOError as e:
            print(f"Error saving {image_type} for {rom_name}: {e}")
            return None

    def download_marquee_art(self, rom_name, filename=None):
        """
        Download marquee art and decals from ArcadeItalia for a given ROM name.
        
        Args:
            rom_name (str): The ROM name (without extension)
            filename (str): Custom filename (defaults to rom_name.png)
            
        Returns:
            str: Path to the downloaded marquee file, or None if download failed
        """
        # URL encode the ROM name for safe URL construction
        encoded_rom_name = quote(rom_name)
        
        # Set default filename if not provided
        if not filename:
            filename = f"{rom_name}.png"
        
        # Download marquee
        marquee_url = f"https://adb.arcadeitalia.net/media/mame.current/marquees/{encoded_rom_name}.png?release=209"
        marquee_path = os.path.join(self.marquee_dir, filename)
        marquee_result = self._download_image(marquee_url, marquee_path, rom_name, "marquee")
        
        # Download decal (gracefully ignore 404)
        decal_filename = filename.replace('.png', '_decal.png')
        decal_url = f"https://adb.arcadeitalia.net/media/mame.current/decals/{encoded_rom_name}.png?release=209"
        decal_path = os.path.join(self.decals_dir, decal_filename)
        decal_result = self._download_image(decal_url, decal_path, rom_name, "decal")
        
        # Download title screen (gracefully ignore 404)
        title_filename = filename.replace('.png', '_title.png')
        title_url = f"https://adb.arcadeitalia.net/media/mame.current/titles/{encoded_rom_name}.png?release=209"
        title_path = os.path.join(self.titles_dir, title_filename)
        title_result = self._download_image(title_url, title_path, rom_name, "title")
        
        # Return the marquee result (primary download)
        return marquee_result

    def scan_and_create_cabinet_art(self):
        """
        Scan NRAN_PACK directory and create cabinet art from all marquees and decals.
        
        Creates:
        - Front art from marquees in NRAN_PACK/marquees/
        - Side art from decals in NRAN_PACK/decals/
        - Saves to NRAN_PACK/cabinet_art/
        """
        print("Scanning NRAN_PACK directory for artwork...")
        print(f"Marquee directory: {self.marquee_dir}")
        print(f"Decals directory: {self.decals_dir}")
        print(f"Output directory: {self.cabinet_art_dir}")
        print()
        
        front_art_count = 0
        side_art_count = 0
        errors = []
        
        # Process marquees to create front art
        if os.path.exists(self.marquee_dir):
            print("Creating front art from marquees...")
            for filename in os.listdir(self.marquee_dir):
                if filename.endswith('.png'):
                    marquee_path = os.path.join(self.marquee_dir, filename)
                    rom_name = filename.replace('.png', '')
                    output_filename = f"{rom_name}_front.png"
                    output_path = os.path.join(self.cabinet_art_dir, output_filename)
                    
                    try:
                        result = self.create_cabinet_art(marquee_path, output_path)
                        print(f"  Created front art: {output_filename}")
                        front_art_count += 1
                    except Exception as e:
                        error_msg = f"Error creating front art for {filename}: {e}"
                        print(f"  ERROR: {error_msg}")
                        errors.append(error_msg)
        else:
            print(f"Marquee directory not found: {self.marquee_dir}")
        
        print()
        
        # Process decals to create side art
        if os.path.exists(self.decals_dir):
            print("Creating side art from decals...")
            for filename in os.listdir(self.decals_dir):
                if filename.endswith('.png') and filename.endswith('_decal.png'):
                    decal_path = os.path.join(self.decals_dir, filename)
                    rom_name = filename.replace('_decal.png', '')
                    output_filename = f"{rom_name}_side.png"
                    output_path = os.path.join(self.cabinet_art_dir, output_filename)
                    
                    try:
                        result = self.create_side_art(decal_path, output_path)
                        print(f"  Created side art: {output_filename}")
                        side_art_count += 1
                    except Exception as e:
                        error_msg = f"Error creating side art for {filename}: {e}"
                        print(f"  ERROR: {error_msg}")
                        errors.append(error_msg)
        else:
            print(f"Decals directory not found: {self.decals_dir}")
        
        # Summary
        print()
        print("Cabinet Art Generation Summary:")
        print(f"  Front art created: {front_art_count}")
        print(f"  Side art created: {side_art_count}")
        print(f"  Total art created: {front_art_count + side_art_count}")
        
        if errors:
            print(f"  Errors encountered: {len(errors)}")
            for error in errors[:5]:  # Show first 5 errors
                print(f"    - {error}")
            if len(errors) > 5:
                print(f"    ... and {len(errors) - 5} more errors")
        else:
            print("  All artwork processed successfully!")

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
                                
                                # Download the marquee to NRAN_PACK/marquees
                                result = self.download_marquee_art(selected_rom)
                                
                                if result:
                                    print(f"Successfully downloaded to: {result}")
                                    print(f"File size: {os.path.getsize(result)} bytes")
                                    
                                    # Ask if user wants to convert to DDS
                                    convert_choice = input("Convert to DDS format? (y/n): ").strip().lower()
                                    if convert_choice in ['y', 'yes']:
                                        dds_result = self.convert_to_dds(result, self.dds_dir)
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
        print("  python image.py --download <rom_name>              # Download marquee to NRAN_PACK/marquees")
        print("  python image.py --interactive                       # Interactive search and download")
        print("  python image.py --create-cabinet-art                # Scan NRAN_PACK and create cabinet art")
        print("  python image.py --all                               # Scan NRAN_PACK and create all cabinet art")
        sys.exit(1)
    
    converter = ImageConverter()
    
    if sys.argv[1] == "--download":
        if len(sys.argv) < 3:
            print("Usage: python image.py --download <rom_name>")
            sys.exit(1)
        
        rom_name = sys.argv[2]
        result = converter.download_marquee_art(rom_name)
        
        if result:
            print(f"Downloaded marquee to: {result}")
        else:
            print(f"Failed to download marquee for: {rom_name}")
    elif sys.argv[1] == "--interactive":
        converter.interactive_marquee_download()
    elif sys.argv[1] == "--create-cabinet-art":
        converter.scan_and_create_cabinet_art()
    elif sys.argv[1] == "--all":
        converter.scan_and_create_cabinet_art()
    else:
        # Original DDS conversion functionality
        if len(sys.argv) != 3:
            print("Usage: python image.py <input_image> <output_dir>")
            sys.exit(1)
        
        converter.convert_to_dds(sys.argv[1], sys.argv[2])
