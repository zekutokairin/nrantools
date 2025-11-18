#!/usr/bin/env python
import subprocess
import json
import tempfile
import hashlib
import os

#URL = "https://www.youtube.com/playlist?list=PLBLdlvve0cQVCbWHF2bqfSWVLrzFGg3w8"
#URL = "https://www.youtube.com/playlist?list=PLBLdlvve0cQWRyicpVj3SgmyrSIpp4D42"
URL = "https://www.youtube.com/playlist?list=PLBLdlvve0cQWvfz2GHuhCqzx0ddoV6g5-"
#USERMEDIAFILE = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\New Retro Arcade Neon\\NewRetroArcade\\Content\\UserMedia.json"
USERMEDIAFILE = "output.json"
LAYOUTFILE = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\New Retro Arcade Neon\\NewRetroArcade\\Content\\Layouts\\Zeku.layout"

MUSICFILE = os.path.join("tests","radio.txt")

VHSDIR = "D:\\VHS\\"

tapeNames = ['Tape1', 'Tape2', 'Tape3', 'Tape4', 'Tape5', 'Tape6', 'Tape7', 'Tape8', 'Tape9', 'Tape10', 
 'Tape11', 'Tape12', 'Tape13', 'Tape14', 'Tape16', 'Tape15', 'Tape17', 'Tape18', 'Tape19', 'Tape20', 
 'Tape21', 'Tape22', 'Tape23', 'Tape24', 'Tape25', 'Tape26', 'Tape27', 'Tape28', 'Tape29']
vhsNames = ['VHSTape1', 'VHSTape3', 'VHSTape4', 'VHSTape5', 'VHSTape6', 'VHSTape7', 'VHSTape8', 'VHSTape9', 'VHSTape10']

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
        
    """
    with open(MEDIAFILE) as fp:
        music_json = json.load(fp)
        # TODO: finish returning the dictionary here
    """

def downloadTape(url):
    #outputPath = os.path.join(VHSDIR)
    return subprocess.run(['yt-dlp','-o', VHSDIR+f'%(id)s', '-f','bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',url])

def parseYTPlaylist(playlist_url):
    # With the given Youtube playlist, return a dictionary with keys ID, Name, URL
    t = tempfile.NamedTemporaryFile(delete=False)
    TMPFILE = t.name
    subprocess.run(['yt-dlp','--flat-playlist','-i','--print-to-file','id,title,url',TMPFILE,playlist_url])

    # TODO: Download the videos to output directory, should skip/continue where necessary
    #subprocess.run(['-f',"bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"

    # Backlog will be a list of dict return
    vhstapes = []

    import code
    with open(TMPFILE, encoding='utf8') as urlfile:
            index = 0 
            lines = urlfile.readlines()
            print(len(lines))
            for index in range(0, len(lines)-1):
                print(index)
                vid_id = "VHSTape_"+lines[index].strip()
                title = lines[index+1].strip()
                url = lines[index+2].strip()

                vhstapes.append({"ID":vid_id,"Name":title,"URL":url})
                
                index += 3
                if index > len(lines)-1:
                    break
                else:
                    continue

    return vhstapes

if __name__ == "__main__":
    #musictapes = parseMusicFile()
    #vhstapes = parseYTPlaylist(URL)
    
    # TODO: Download the tapes themselves
    tempurl = "https://www.youtube.com/watch?v=PBGQvbwCg60"
    downloadTape(tempurl)
                          
    # TODO: Form the XML output, not CSV here
    for video in vhstapes:
        line = ",".join([video['Name'],video['URL'],'VHSTape',"","Yes"])
        csv += line
        csv += "\n"
