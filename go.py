#!/usr/bin/env python3

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nrantools.image import ImageConverter

def test_marquee_download():
    """Test the marquee download functionality."""
    converter = ImageConverter()
    
    # Test with a common arcade ROM name
    test_roms = [
        "chinagat"
    ]
    
    print("Testing marquee downloads...")
    
    for rom_name in test_roms:
        print(f"\nDownloading marquee for: {rom_name}")
        result = converter.download_marquee_art(rom_name, "downloaded_marquees")
        
        if result:
            print(f"✓ Success: {result}")
        else:
            print(f"✗ Failed to download marquee for {rom_name}")

if __name__ == "__main__":
    test_marquee_download()
