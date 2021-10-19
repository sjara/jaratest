"""
Test loading video info.
"""

import imp
import os
from jaratoolbox import settings

subject = 'test000'
infoVideosPath = os.path.join(settings.INFOVIDEO_PATH, subject+'_infovideos.py')
infoVideos = imp.load_source('module.name', infoVideosPath)

print(infoVideos.videos)


