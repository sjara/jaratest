'''
Information about videos.
'''

from jaratoolbox import videoinfo

        
subject = 'pure001'
videos = videoinfo.Videos(subject)
cameraParams = videoinfo.cameraParams['IR_webcam_640x480_30fps_VP9']

videos.add_session('2021-09-28', 'positiveControl',
                   'pure001_20210928_syncVisibleNoSound_01.mkv',
                   'pure001_detectsound_20210928_syncVisibleNoSound_01.h5',
                   cameraParams) 
                   
videos.add_session('2021-09-28', 'negativeControl',
                   'pure001_20210928_NoSound_01.mkv',
                   'pure001_detectsound_20210928_syncNoSound_01.h5',
                   cameraParams)

videos.add_session('2021-09-28', 'chordTrain',
                   'pure001_20210928_syncSound_01.mkv',
                   'pure001_detectsound_20210928_syncSound_01.h5',
                   cameraParams)
