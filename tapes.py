#!/usr/bin/env python
import subprocess
import yt_dlp
import tempfile
import itertools

URL = "https://www.youtube.com/playlist?list=PLBLdlvve0cQVCbWHF2bqfSWVLrzFGg3w8"

with tempfile.NamedTemporaryFile(delete_on_close=False) as fp:
    subprocess.run(['yt-dlp','--flat-playlist','--print-to-file','title:url',fp.name,URL])
    with open(fp.name) as url_file:
        for title,url in itertools.zip_longest(*[url_file]*2):
            print("%s:%s" % (title,url))


def ytBacklog():
    # get user playlist public/unlinked
    # return list of urls to write into CSV
    pass

