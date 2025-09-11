#!/usr/bin/env python

# FIXME: Test file, everything in here should be moved once working

import json
import os
import hashlib
import tempfile
import subprocess

URL = "https://www.youtube.com/playlist?list=PLBLdlvve0cQVCbWHF2bqfSWVLrzFGg3w8"
USERMEDIAFILE = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\New Retro Arcade Neon\\NewRetroArcade\\Content\\UserMedia.json"
LAYOUTFILE = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\New Retro Arcade Neon\\NewRetroArcade\\Content\\Layouts\\Zeku.layout"

MUSICFILE = os.path.join("tests","radio.txt")

tapeNames = ['Tape1', 'Tape2', 'Tape3', 'Tape4', 'Tape5', 'Tape6', 'Tape7', 'Tape8', 'Tape9', 'Tape10', 
 'Tape11', 'Tape12', 'Tape13', 'Tape14', 'Tape16', 'Tape15', 'Tape17', 'Tape18', 'Tape19', 'Tape20', 
 'Tape21', 'Tape22', 'Tape23', 'Tape24', 'Tape25', 'Tape26', 'Tape27', 'Tape28', 'Tape29']
vhsNames = ['VHSTape1', 'VHSTape3', 'VHSTape4', 'VHSTape5', 'VHSTape6', 'VHSTape7', 'VHSTape8', 'VHSTape9', 'VHSTape10']

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
            musictapes.append({"ID":tape_id,"Name":name,"URL":url})
    
    return musictapes
        
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
    musictapes = parseMusicFile()
    vhstapes = parseVideoTapes(URL)
    usermedia_json = None
    with open(USERMEDIAFILE) as fp:
        usermedia_json = json.load(fp)
    usermedia_json.extend(musictapes)
    usermedia_json.extend(vhstapes)
    # TODO: sort entries by Tape, VHS
    # TODO: eliminate duplicates

    """
    with open(USERMEDIAFILE,"w") as fp:
        json.dump(usermedia_json,fp,indent=4)
    """
        
    with open(LAYOUTFILE) as fp:
        a = json.load(fp)
        import code
        code.interact(local=locals())
        tapes = a.get("Tapes")

