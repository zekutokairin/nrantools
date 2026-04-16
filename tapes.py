#!/usr/bin/env python
import argparse
import subprocess
import json
import tempfile
import hashlib
import os
import random

import pathlib

import yt_dlp

import code

#URL = "https://www.youtube.com/playlist?list=PLBLdlvve0cQVCbWHF2bqfSWVLrzFGg3w8"
#URL = "https://www.youtube.com/playlist?list=PLBLdlvve0cQWRyicpVj3SgmyrSIpp4D42"
#URL = "https://www.youtube.com/playlist?list=PLBLdlvve0cQWvfz2GHuhCqzx0ddoV6g5-"
#URL = "https://www.youtube.com/playlist?list=PLBLdlvve0cQVpyt73l8hqRNQAxTdIqqpQ"


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

def parseMediaDir(path):
    folder_path = pathlib.Path(path)
    tape_list = [str(f.resolve()) for f in folder_path.iterdir() if f.is_file()]

    return tape_list

if __name__ == "__main__":
    # 1. Initialize the parser
    parser = argparse.ArgumentParser(description="A retro media collector script.")

    # 2. Add arguments
    # -c for cassette
    parser.add_argument('-c', '--cassette', type=str, help='Directory full of music files to randomly select into cassettes.')
    
    # -v for vhs
    parser.add_argument('-v', '--vhs', type=str, help='Movie title on the VHS tape')

    # 3. Parse the arguments
    args = parser.parse_args()

    # 4. Access the variables
    if args.cassette:
        print(f"Cassette variable: {args.cassette}")
        tape_list = parseMediaDir(args.cassette)
        if len(tape_list) < 29:
            for n in range(len(tape_list), 29):
                tape_list.append(tape_list[0])

        for i in range(0, len(tape_list)):
            line = "<%s Name=\"%s\" URL=\"%s\" />" % (tapeNames[i], pathlib.Path(tape_list[i]).stem,tape_list[i])
            print(line)
    
    if args.vhs:
        print(f"VHS variable: {args.vhs}")
        vhs_list = parseMediaDir(args.vhs)
        if len(vhs_list) < 10:
            for n in range(len(vhs_list), 10):
                vhs_list.append(vhs_list[0])

        for i in range(0, len(vhs_list)):
            line = "<%s Name=\"%s\" URL=\"%s\" />" % (vhsNames[i], pathlib.Path(vhs_list[i]).stem,vhs_list[i])
            print(line)

    
    #TODO: Read in the files in the directory to create a list of vhs/tapes
    #random.shuffle(vhstapes)
    """
    for i in range(0, len(vhsNames)):
        tape = vhstapes[i]
        #downloadTape(tempurl)
        localpath = os.path.join(VHSDIR, tape['ID'])
        
        #line = "<VHSTape1 Name=\"" + tape['Name'] + "URL=\"" + localpath + "\" />"
        line = "<%s Name=\"%s\" URL=\"%s\" />" % (vhsNames[i], tape['Name'],localpath)
        print(line)
    """
