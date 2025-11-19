#!/usr/bin/env python
import subprocess
import json
import tempfile
import hashlib
import os
import random

import yt_dlp

import code

#URL = "https://www.youtube.com/playlist?list=PLBLdlvve0cQVCbWHF2bqfSWVLrzFGg3w8"
#URL = "https://www.youtube.com/playlist?list=PLBLdlvve0cQWRyicpVj3SgmyrSIpp4D42"
#URL = "https://www.youtube.com/playlist?list=PLBLdlvve0cQWvfz2GHuhCqzx0ddoV6g5-"
URL = "https://www.youtube.com/playlist?list=PLBLdlvve0cQVpyt73l8hqRNQAxTdIqqpQ"


#USERMEDIAFILE = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\New Retro Arcade Neon\\NewRetroArcade\\Content\\UserMedia.json"
USERMEDIAFILE = "output.json"
LAYOUTFILE = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\New Retro Arcade Neon\\NewRetroArcade\\Content\\Layouts\\Zeku.layout"

MUSICFILE = os.path.join("tests","radio.txt")

VHSDIR = "D:\\VHS\\"

# This is used to get the name of the file which was saved using the yt-dlp output format
final_filename = None

tapeNames = ['Tape1', 'Tape2', 'Tape3', 'Tape4', 'Tape5', 'Tape6', 'Tape7', 'Tape8', 'Tape9', 'Tape10', 
 'Tape11', 'Tape12', 'Tape13', 'Tape14', 'Tape16', 'Tape15', 'Tape17', 'Tape18', 'Tape19', 'Tape20', 
 'Tape21', 'Tape22', 'Tape23', 'Tape24', 'Tape25', 'Tape26', 'Tape27', 'Tape28', 'Tape29']
vhsNames = ['VHSTape1', 'VHSTape2', 'VHSTape3', 'VHSTape4', 'VHSTape5', 'VHSTape6', 'VHSTape7', 'VHSTape8', 'VHSTape9', 'VHSTape10']

# TODO: Theory, build database of entries into UserMedia.json, THEN add them in the LayoutFile?
# Lists of radio stations:
#  https://asiadreamradio.torontocast.stream/stations/newstream.html

def parseMusicFile():
    musictapes = []
    with open(MUSICFILE, encoding='utf-8') as fp:
        for line in fp:
            name, url = line.strip().split(",")
            import code
            tape_id = "Tape"+ hashlib.md5(url.encode('utf-8')).hexdigest()
            print("%s:%s:%s" % (tape_id,name,url))
            musictapes.append({"ID":tape_id,"Name":name,"URL":url})
    
    return musictapes
        
def downloadTape(url):
    #outputPath = os.path.join(VHSDIR)
    return subprocess.run(['yt-dlp','-o', VHSDIR+f'%(id)s', '-f','bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',url])

def yt_dlp_monitor(self, d):
    final_filename  = d.get('info_dict').get('_filename')

ydl_opts = {
    "outtmpl": VHSDIR + '%(id)s.%(ext)s',  # this is where you can edit how you'd like the filenames to be formatted
    "progress_hooks": [yt_dlp_monitor]  # here's the function we just defined
    }

myopts = {
    "extract_flat":"True",
    "outtmpl": VHSDIR + '%(id)s.%(ext)s',  # this is where you can edit how you'd like the filenames to be formatted
    'format': 'bestvideo+bestaudio/best',
    'merge_output_format':'mp4'
}

def test(playlist_url):
    # Getting the filename described in:
    #  https://stackoverflow.com/questions/74157935/getting-the-file-name-of-downloaded-video-using-yt-dlp
    with yt_dlp.YoutubeDL(myopts) as ydl:
        vid = ydl.download(playlist_url)
        print(final_filename)
        #code.interact(local=locals())

def parseYTPlaylist(playlist_url):
    import code
    
    # With the given Youtube playlist, return a dictionary with keys ID, Name, URL
    t = tempfile.NamedTemporaryFile(delete=False)
    TMPFILE = t.name
    subprocess.run(['yt-dlp','--flat-playlist','-i','--print-to-file','id,title,url',TMPFILE,playlist_url])

    # Backlog will be a list of dict return
    vhstapes = []

    with open(TMPFILE, encoding='utf8') as urlfile:
            index = 0 
            lines = urlfile.readlines()

            while len(lines) > 0:
                vid_id = lines.pop(0).strip()
                title = lines.pop(0).strip()
                url = lines.pop(0).strip()

                vhstapes.append({"ID":vid_id,"Name":title,"URL":url})

    return vhstapes

if __name__ == "__main__":
    test(URL)
    
    raise Exception("Debugging")
    #musictapes = parseMusicFile()
    vhstapes = parseYTPlaylist(URL)
    
    # TODO: Download the tapes themselves by deleting this and giving download tape the real URL
    tempurl = "https://www.youtube.com/watch?v=PBGQvbwCg60"
                          
    import code
    random.shuffle(vhstapes)

    for i in range(0, len(vhsNames)):
        tape = vhstapes[i]
        #downloadTape(tempurl)
        localpath = os.path.join(VHSDIR, tape['ID'])
        
        #line = "<VHSTape1 Name=\"" + tape['Name'] + "URL=\"" + localpath + "\" />"
        line = "<%s Name=\"%s\" URL=\"%s\" />" % (vhsNames[i], tape['Name'],localpath)
        print(line)
