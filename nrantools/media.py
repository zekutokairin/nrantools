#!/usr/bin/env python3

import argparse
import subprocess
import json
import tempfile
import hashlib
import os
import random
import pathlib
import yt_dlp

class MediaProcessor:
    """Processes VHS tapes and cassette tapes for New Retro Arcade:Neon."""
    
    def __init__(self, usermedia_file="output.json", layout_file=None, vhs_dir="D:\\VHS\\"):
        self.USERMEDIAFILE = usermedia_file
        self.LAYOUTFILE = layout_file or "C:\\Program Files (x86)\\Steam\\steamapps\\common\\New Retro Arcade Neon\\NewRetroArcade\\Content\\Layouts\\Zeku.layout"
        self.VHSDIR = vhs_dir
        
        self.tape_names = ['Tape1', 'Tape2', 'Tape3', 'Tape4', 'Tape5', 'Tape6', 'Tape7', 'Tape8', 'Tape9', 'Tape10', 
                          'Tape11', 'Tape12', 'Tape13', 'Tape14', 'Tape16', 'Tape15', 'Tape17', 'Tape18', 'Tape19', 'Tape20', 
                          'Tape21', 'Tape22', 'Tape23', 'Tape24', 'Tape25', 'Tape26', 'Tape27', 'Tape28', 'Tape29']
        self.vhs_names = ['VHSTape1', 'VHSTape2', 'VHSTape3', 'VHSTape4', 'VHSTape5', 'VHSTape6', 'VHSTape7', 'VHSTape8', 'VHSTape9', 'VHSTape10']

    def parse_music_file(self, music_file):
        """Parse music file with format: name,url per line."""
        musictapes = []
        with open(music_file, encoding='utf-8') as fp:
            for line in fp:
                if line.strip():
                    name, url = line.strip().split(",")
                    tape_id = "Tape" + hashlib.md5(url.encode('utf-8')).hexdigest()
                    print("%s:%s:%s" % (tape_id, name, url))
                    musictapes.append({"ID": tape_id, "Name": name, "URL": url})
        
        return musictapes

    def download_tape(self, url):
        """Download a tape from YouTube using yt-dlp."""
        return subprocess.run(['yt-dlp', '-o', self.VHSDIR + f'%(id)s', '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', url])

    def parse_yt_playlist(self, playlist_url):
        """Parse YouTube playlist and return list of videos."""
        t = tempfile.NamedTemporaryFile(delete=False)
        tmpfile = t.name
        subprocess.run(['yt-dlp', '--flat-playlist', '-i', '--print-to-file', 'id,title,url', tmpfile, playlist_url])

        vhstapes = []
        with open(tmpfile, encoding='utf8') as urlfile:
            index = 0 
            lines = urlfile.readlines()

            while len(lines) > 0:
                vid_id = lines.pop(0).strip()
                title = lines.pop(0).strip()
                url = lines.pop(0).strip()

                vhstapes.append({"ID": vid_id, "Name": title, "URL": url})

        return vhstapes

    def parse_media_dir(self, path):
        """Parse a directory of media files and return list of file paths."""
        folder_path = pathlib.Path(path)
        tape_list = [str(f.resolve()) for f in folder_path.iterdir() if f.is_file()]
        return tape_list

    def generate_cassette_tapes(self, media_dir):
        """Generate cassette tape XML entries from media directory."""
        tape_list = self.parse_media_dir(media_dir)
        if len(tape_list) < 29:
            for n in range(len(tape_list), 29):
                tape_list.append(tape_list[0])

        for i in range(0, len(tape_list)):
            line = "<%s Name=\"%s\" URL=\"%s\" />" % (self.tape_names[i], pathlib.Path(tape_list[i]).stem, tape_list[i])
            print(line)

    def generate_vhs_tapes(self, media_dir):
        """Generate VHS tape XML entries from media directory."""
        vhs_list = self.parse_media_dir(media_dir)
        if len(vhs_list) < 10:
            for n in range(len(vhs_list), 10):
                vhs_list.append(vhs_list[0])

        for i in range(0, len(vhs_list)):
            line = "<%s Name=\"%s\" URL=\"%s\" />" % (self.vhs_names[i], pathlib.Path(vhs_list[i]).stem, vhs_list[i])
            print(line)

    def process_command_line(self):
        """Process command line arguments for media processing."""
        parser = argparse.ArgumentParser(description="A retro media collector script.")
        parser.add_argument('-c', '--cassette', type=str, help='Directory full of music files to randomly select into cassettes.')
        parser.add_argument('-v', '--vhs', type=str, help='Movie title on the VHS tape')
        
        args = parser.parse_args()

        if args.cassette:
            print(f"Cassette variable: {args.cassette}")
            self.generate_cassette_tapes(args.cassette)
        
        if args.vhs:
            print(f"VHS variable: {args.vhs}")
            self.generate_vhs_tapes(args.vhs)

if __name__ == "__main__":
    processor = MediaProcessor()
    processor.process_command_line()
