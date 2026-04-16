# nrantools

A Python toolkit for managing New Retro Arcade:Neon content. This package provides utilities for organizing ROM cartridges, converting images, processing media files, and verifying arcade content.

## Installation

### From Source
```bash
git clone <repository-url>
cd nrantools
pip install -e .
```

### Dependencies
The package requires the following dependencies:
- pandas >= 1.3.0
- Pillow >= 8.0.0  
- Wand >= 0.6.0
- yt-dlp >= 2023.1.0
- textual >= 0.1.0

## Usage

### As a Python Package

```python
from nrantools import CartridgeManager, MediaProcessor, ImageConverter, ContentVerifier

# Manage ROM cartridges and artwork
cart_manager = CartridgeManager(pack_dir="/path/to/roms", output_dir="output")
cart_manager.process_cartridges()

# Process media files (VHS tapes, cassettes)
media_processor = MediaProcessor()
media_processor.generate_cassette_tapes("/path/to/music")
media_processor.generate_vhs_tapes("/path/to/videos")

# Convert images to DDS format
image_converter = ImageConverter()
image_converter.convert_to_dds("input.jpg", "output_dir")

# Verify content integrity
verifier = ContentVerifier()
csv_data = verifier.verify_content("/path/to/roms")
```

### Command Line Tools

After installation, you can use the following command-line tools:

```bash
# Process cartridges
nrantools-carts

# Process media files  
nrantools-media --cassette /path/to/music --vhs /path/to/videos

# Convert images
nrantools-image input.jpg output_dir

# Verify content
nrantools-verify /path/to/content

# Launch UI
nrantools-ui
```

## Module Structure

- **cartridge.py**: `CartridgeManager` - Handles ROM cartridges and artwork processing
- **media.py**: `MediaProcessor` - Processes VHS tapes and cassette tapes
- **image.py**: `ImageConverter` - Converts images and creates cabinet art
- **verification.py**: `ContentVerifier` - Validates and verifies arcade content
- **ui.py**: `ClockApp` - Simple clock UI using Textual framework
- **utils.py**: `Utils` - Utility functions for common operations

## Environment Variables

- `NRAN_DEBUG`: Enable debug mode
- `NRAN_PACK`: Path to your ROM pack directory
- `NRAN_CONTENT_DIR`: Path to NRAN Content directory (default: Steam installation path)

## Original Scripts for importing and maintaining your personal arcade in N:RAN

# Dev Setup
- To launch directly into an arcade, add launch options:
    - `-defaultmap=newretroarcade_neon` or `-defaultmap=newretroarcade`
- Copy in ArcadeManager
- Copy in Dado Pack
- Replace `NewRetroArcade\Plugins\VlcMedia\ThirdParty\real-youtube-dl` with 64 bit yt-dlp
- Add `<picodrive_renderer value="accurate" / >`  to ArcadeEmulatorOptions.xml
- Use HOME key to reload arcade in real time? (TODO: Try this)

- Use non-merged ROMs for better performance
- remember LATEST qsound.zip for CPS2 games

- Check if it gets the layout from the .ini file:
Q: How do I pick a layout as default?
A: You can choose a default layout either by adding ArcadeLayout=[LAYOUT NAME HERE] to GameUserSettings.ini or by adding -ArcadeLayout=[LAYOUT NAME HERE] as a launch option. You can also launch directly into a layout in the Arcade Builder by right clicking on it.
- I THINK carts, etc. need to be defined in the json file and then specified in the XML or Vice Versa

# Notes
- ArcadeLayout can be None or a specified Layout
- GameMusicVolume is for the attract movies

## Tapes
- The actual XML to load things is the ArcadeTapes.xml
    - Parse them with a Python library:
        - xml? lxml?
    - `Content/UserMedia.json` is where the tapes/VHS data is stored
        - Is this just the database where things are eventually taken to the xml?
        - Does the layout file use the json rather than the XML or something?
- If a layout is not specified in GameUserSettings.ini, it pulls straight from ArcadeTapes.xml
    - If a layout IS specified, it goes to that .layout which is a JSON file
    - `Content/UserMedia.json` is where the tapes/VHS data is stored (I think this is just for ArcadeManager maybe??)
        - Or does ArcadeManager just use the CSV files?

## Configs
- Create XML files for cartridges
    - Tapes: from list of files and radio stations
    - Cartridges: from ROM list and cover arts
    - Arcades: from ROM list and side art and banner
- GameUserSettings
    - Set Layout file
    - Turn off trash

# Tested working (After Dado pack)
- Arcade
- NES
- SNES
- Genesis
- GBA
- GameGear
- Gamebro (Gameboy w/backlight)
- Music Tapes (http)
- VHS (Local video)
- VHS (Remote file share)

# Needs Testing
- VHS
- Music Tapes (https appears to not work)

# Quality of Life
- Automate fixing GameUserSettings.ini
    - Removing trash, etc.
# Problems
- Video files with more than one audio track have no audio in VHS mode
    - Testing with Haikyuu ep1 resulted in no audio
    - MKV with multiple audio tracks AAC, but why did NONE play?
    - Mad Men Ep 5 also tested, multiple audio tracks seem to break it

===================================
# Potential solutions

# Download latest retroarch core nightlies

# Need to double check these
- Try Genesis Plus GX core?
- In GameUserSettings, what is emulatormode = EM_BALANCED? Is there a performance?

# (Optional) Remove assorted trash
## in New Retro Arcade Neon\NewRetroArcade\Saved\Config\WindowsNoEditor directory, open GameUserSettings and remove trash
