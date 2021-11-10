'''
Information about videos.
'''

from jaratoolbox import videoinfo

        
subject = 'chad049'
videos = videoinfo.Videos(subject)
cameraParams = videoinfo.cameraParams['IR_webcam_640x480_30fps_VP9']

videos.add_session('2020-10-22', 'positiveControl',
                   'chad049_detect_sound_pos_20201022_config0.mvk',
                   '',
                   cameraParams) 
                   
videos.add_session('2020-12-10', 'negativeControl',
                   'chad049_detect_sound_neg_20201210_config0.mkv',
                   '',
                   cameraParams)
                   
videos.add_session('2020-12-10', 'experimental',
                   'chad049_detect_sound_sound_20201210_config0.mkv',
                   '',
                   cameraParams)
