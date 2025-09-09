# nrantools
Scripts for importing and maintaining your personal arcade in N:RAN

# Dev Setup
- Use `-defaultmap=newretroarcade_neon` in the launch options to skip main menu
- Copy in Dado Pack
- Replace `NewRetroArcade\Plugins\VlcMedia\ThirdParty\real-youtube-dl` with 64 bit yt-dlp

# Notes
## Tapes
- The actual XML to load things is the ArcadeTapes.xml
    - Parse them with a Python library:
        - xml? lxml?
    - `Content/UserMedia.json` is where the tapes/VHS data is stored
- Check what version of VLC works with local videos

# Tested working (After Dado pack)
- Arcade
- SNES
- Gamebro 

# Needs Testing
- NES
- Genesis

# Problems

===================================
# Potential solutions
# From working clean install, steps to take:

# Download latest retroarch core nightlies


# Need to double check these
- Latest vlc core to avoid dll warnings?
- Try disabling more ASLR settings
- Try Genesis Plus GX core?

# (Optional) Remove assorted trash
## in New Retro Arcade Neon\NewRetroArcade\Saved\Config\WindowsNoEditor directory, open GameUserSettings and remove trash


## Potential problem: if we're generating completely correct CSVs and Arcade
Manager still doesn't like them, there's not much else to do besides make our
own XMLs?
