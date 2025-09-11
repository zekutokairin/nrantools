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
## Tapes
- If a layout is not specified in GameUserSettings.ini, it pulls straight from ArcadeTapes.xml
- If a layout IS specified, it goes to that .layout which is a JSON file
    - `Content/UserMedia.json` is where the tapes/VHS data is stored (I think this is just for ArcadeManager maybe??)
- Check what version of VLC works with local videos

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

# Problems
- Automate fixing GameUserSettings.ini


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
