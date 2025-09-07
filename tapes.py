#!/usr/bin/env python

import yt_dlp

#TODO: Get playlist name/url
PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLBLdlvve0cQWCAEHu7i7vohfcHHTbo5VR"


ytdl_opts = {'extract_flat': 'discard_in_playlist',
 'fragment_retries': 10,
 'ignoreerrors': 'only_download',
 'postprocessors': [{'key': 'FFmpegConcat',
                     'only_multi_video': True,
                     'when': 'playlist'}],
 'retries': 10,
 'warn_when_outdated': True}

def ytBacklog():
    # get user playlist public/unlinked
    # return list of urls to write into CSV
    pass

if __name__ == "__main__":
	with yt_dlp.YoutubeDL(ytdl_opts) as ydl:
		a = ydl.download([PLAYLIST_URL])
		import code
		code.interact(local=locals())
