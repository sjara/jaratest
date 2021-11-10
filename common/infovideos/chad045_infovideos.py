'''
Information about videos.
'''

from jaratoolbox import videoinfo

        
subject = 'chad045'
videos = videoinfo.Videos(subject)
cameraParams = videoinfo.cameraParams['IR_webcam_640x480_30fps_VP9']

videos.add_session('2020-10-30', 'positiveControl',
                   'chad045_detect_sound_pos_20201030_config0.mkv',
                   '',
                   cameraParams) 
videos.add_session('2020-11-09', 'positiveControl',
                   'chad045_detect_sound_pos_20201109_config0.mkv',
                   '',
                    cameraParams) 
videos.add_session('2020-11-02', 'positiveControl',
                   'chad045_detect_sound_pos_20201102_config0.mkv',
                   '',
                   cameraParams)
                   
videos.add_session('2020-11-02', 'negativeControl',
                   'chad045_detect_sound_neg_20201102_config0.mkv',
                   '',
                   cameraParams)
videos.add_session('2020-12-10', 'negativeControl',
                   'chad045_detect_sound_neg_20201210_config0.mkv',
                   '',
                   cameraParams)
                   
videos.add_session('2020-12-10', 'experimental',
                   'chad045_detect_sound_neg_20201210_config0.mkv',
                   '',
                   cameraParams)
