'''
Information about videos.
'''

from jaratoolbox import videoinfo

        
subject = 'chad048'
videos = videoinfo.Videos(subject)
cameraParams = videoinfo.cameraParams['IR_webcam_640x480_30fps_VP9']

videos.add_session('2020-10-22', 'positiveControl',
                   'chad048_detect_sound_pos_20201022_config0.mvk',
                   '',
                   cameraParams) 
videos.add_session('2020-11-09', 'positiveControl',
                   'chad048_detect_sound_pos_20201109_config0.mkv',
                   '',
                    cameraParams) 
               
videos.add_session('2020-12-10', 'negativeControl',
                   'chad048_detect_sound_neg_20201210_config0.mkv',
                   '',
                   cameraParams)
                   
videos.add_session('2020-12-10', 'experimental',
                   'chad048_detect_sound_sound_20201210_config0.mkv',
                   '',
                   cameraParams)
