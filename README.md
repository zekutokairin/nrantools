# nrantools
Scripts for importing and maintaining your personal arcade in N:RAN

# Dev Setup
- Use `-defaultmap=newretroarcade_neon` in the launch options to skip main menu
- Copy in Dado Pack
- Replace `NewRetroArcade\Plugins\VlcMedia\ThirdParty\real-youtube-dl` with 64 bit yt-dlp

- Check if it gets the layout from the .ini file:
Q: How do I pick a layout as default?
A: You can choose a default layout either by adding ArcadeLayout=[LAYOUT NAME HERE] to GameUserSettings.ini or by adding -ArcadeLayout=[LAYOUT NAME HERE] as a launch option. You can also launch directly into a layout in the Arcade Builder by right clicking on it.
- I THINK carts, etc. need to be defined in the json file and then specified in the XML or Vice Versa

# Notes
- ArcadeLayout can be None or a specified Layout
- GameMusicVolume is for the the attract, I think between 0 and 1. BUT, sometimes values in between aren't working right?

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
- SNES
- Gamebro 
- VHS (Youtube)
- Music Tapes (http)

# Needs Testing
- NES
- Genesis
- VHS (Local video)
- VHS (Remote file share)
- Music Tapes (https appears to not work)

# Quality of Life
- Automate fixing GameUserSettings.ini
    - Removing trash, etc.
# Problems
- Testing with Haikyuu ep1 resulted in no audio
    - MKV with multiple audio tracks AAC, but why did NONE play?
    - Mad Men Ep 5 also tested, multiple audio tracks seem to break it


===================================
# Potential solutions
# From working clean install, steps to take:

# Download latest retroarch core nightlies

# Need to double check these
- Latest vlc core to avoid dll warnings?
    - Just updating yt-dlp was enough for youtube
    - If we need a newer VLC plugin core, that may require more work
- Try disabling more ASLR settings
     - I don't think these are necessary
- Try Genesis Plus GX core?
- In GameUserSettings, what is emulatormode = EM_BALANCED? Is there a performance?

# (Optional) Remove assorted trash
## in New Retro Arcade Neon\NewRetroArcade\Saved\Config\WindowsNoEditor directory, open GameUserSettings and remove trash
