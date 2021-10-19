'''
Information about videos.
'''

from jaratoolbox import videoinfo

        
subject = 'test000'
videos = videoinfo.Videos(subject)
cameraParams = videoinfo.cameraParams['IR_webcam_640x480_30fps_VP9']

videos.add_session('2021-10-17', 'testSession',
                   'test000_20211017a.mkv',
                   'test000_testsound_20211017a.h5',
                   cameraParams)

videos.add_session('2021-10-18', 'realSession',
                   'test000_20211018testSession.mkv',
                   'test000_testsound_20211018testSession.h5',
                   cameraParams)

