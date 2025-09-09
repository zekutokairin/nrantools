#!/usr/bin/env python
import subprocess
import yt_dlp
import tempfile
import itertools

URL = "https://www.youtube.com/playlist?list=PLBLdlvve0cQVCbWHF2bqfSWVLrzFGg3w8"

# TODO: Theory, build database of entries into json, THEN add them in the Layout?
# Lists of radio stations:
#   https://asiadreamradio.torontocast.stream/stations/newstream.html

def ytBacklog(playlist_url):
    # get user playlist public/unlinked
    # return list of urls to write into CSV
    t = tempfile.NamedTemporaryFile(delete=False)
    #TMPFILE = "D://transfar//urls.txt"
    TMPFILE = t.name
    print(t.name)

    subprocess.run(['yt-dlp','--flat-playlist','-i','--print-to-file','title,url',TMPFILE,playlist_url])

    # Backlog will be a list of tuples we return
    backlog = []

    with open(TMPFILE) as urlfile:
        for title in urlfile:
            title = title.strip()
            url = next(urlfile).strip()
            backlog.append((title,url))

    return backlog

if __name__ == "__main__":
    # TODO: Radio Stations
    yt_videos = ytBacklog(URL)
    import code
    code.interact(local=locals())
