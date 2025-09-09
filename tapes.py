#!/usr/bin/env python
import subprocess
import json
import tempfile
import hashlib
import os

URL = "https://www.youtube.com/playlist?list=PLBLdlvve0cQVCbWHF2bqfSWVLrzFGg3w8"
MEDIAFILE = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\New Retro Arcade Neon\\NewRetroArcade\\Content\\UserMedia.json"
LAYOUTFILE = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\New Retro Arcade Neon\\NewRetroArcade\\Content\\Layouts\\DadoPack.layout"

MUSICFILE = os.path.join("tests","radio.txt")

# TODO: Theory, build database of entries into UserMedia.json, THEN add them in the LayoutFile?
# Lists of radio stations:
#   https://asiadreamradio.torontocast.stream/stations/newstream.html

def parseMusicFile():
    musictapes = []
    with open(MUSICFILE, encoding='utf-8') as fp:
        for line in fp:
            name, url = line.strip().split(",")
            import code
            #code.interact(local=locals())
            tape_id = "Tape"+ hashlib.md5(url.encode('utf-8')).hexdigest()
            print("%s:%s:%s" % (tape_id,name,url))
        
    """
    with open(MEDIAFILE) as fp:
        music_json = json.load(fp)
        # TODO: finish returning the dictionary here
    """

def parseVideoTapes(playlist_url):
    # With the given Youtube playlist, return a dictionary with keys ID, Name, URL
    t = tempfile.NamedTemporaryFile(delete=False)
    TMPFILE = t.name
    subprocess.run(['yt-dlp','--flat-playlist','-i','--print-to-file','id,title,url',TMPFILE,playlist_url])

    # Backlog will be a list of dictwe return
    vhstapes = []

    with open(TMPFILE) as urlfile:
        for vid_id in urlfile:
            vid_id = "VHSTape"+vid_id.strip()
            title = next(urlfile).strip()
            url = next(urlfile).strip()

            vhstapes.append({"ID":vid_id,"Name":title,"URL":url})

    return vhstapes

def writeUserMedia(music_dict,video_dict):
    with open(MEDIAFILE,'w'):
        pass

if __name__ == "__main__":
    # TODO: Radio Stations
    music_dict = parseMusicFile()
    #vhs_dict = parseVideoTapes(URL)
    import code
    #code.interact(local=locals())
