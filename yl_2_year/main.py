# -*- coding: utf-8 -*-

from youtube_dl import YoutubeDL
from youtube_dl.utils import DownloadError
from pprint import pprint

dl_options = {'verbose': True}

# https://twitter.com/PPathole/status/1455785718043734024
# https://twitter.com/ParkKrasnodar/status/1458876348265644033
# https://www.youtube.com/watch?v=LXb3EKWsInQ

with YoutubeDL(dl_options) as ydl:
    meta = ydl.extract_info('https://www.youtube.com/watch?v=BXF3SCuewJA',
                            download=False)
    pprint(meta)
    # ydl.download(['https://www.youtube.com/watch?v=BXF3SCuewJA'])
