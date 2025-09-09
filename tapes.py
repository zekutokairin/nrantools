#!/usr/bin/env python
import subprocess
import yt_dlp
import tempfile
import itertools

URL = "https://www.youtube.com/playlist?list=PLBLdlvve0cQVCbWHF2bqfSWVLrzFGg3w8"

t = tempfile.NamedTemporaryFile(delete=False)
#TMPFILE = "D://transfar//urls.txt"
TMPFILE = t.name
print(t.name)

#with ) as fp:
subprocess.run(['yt-dlp','--flat-playlist','-i','--print-to-file','title,url',TMPFILE,URL])

"""
with open(fp.name) as url_file:
    for title,url in itertools.zip_longest(*[url_file]*2):
        print("%s:%s" % (title,url))

"""

#TODO: Get playlist name/url

def ytBacklog():
    # get user playlist public/unlinked
    # return list of urls to write into CSV
    pass

