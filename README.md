# nrantools
Scripts for importing and maintaining your personal arcade in N:RAN

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
