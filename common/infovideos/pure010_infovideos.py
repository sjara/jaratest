'''
Information about videos.
'''

from jaratoolbox import videoinfo

        
subject = 'pure003'
videos = videoinfo.Videos(subject)
cameraParams = videoinfo.cameraParams['IR_webcam_640x480_30fps_VP9']

videos.add_session('2022-02-15', '2chords',
                   'pure010_20220215_2Sounds_113_2Sconfig9.mp4',
                   'pure010_20220215_2Sounds_113_2Sconfig9.h5',
                   cameraParams) 
                   
videos.add_session('2022-02-15', '2chords',
                   'pure010_20220215_2Sounds_114_2Sconfig9.mp4',
                   'pure010_20220215_2Sounds_114_2Sconfig9.h5',
                   cameraParams)
                   
videos.add_session('2022-02-15', '2chords',
                   'pure010_20220215_2Sounds_115_2Sconfig9.mp4',
                   'pure010_20220215_2Sounds_115_2Sconfig9.h5',
                   cameraParams)

videos.add_session('2022-02-15', '2chords',
                   'pure010_20220215_2Sounds_115_2Sconfig9.mp4',
                   'pure010_20220215_2Sounds_115_2Sconfig9.h5',
                   cameraParams)

videos.add_session('2022-02-16', 'chord',
                   'pure010_20220216_syncSound_76_config20.mp4',
                   'pure010_20220216_syncSound_76_config20.h5',
                   cameraParams)                                     

videos.add_session('2022-02-16', 'chord',
                   'pure010_20220216_syncSound_77_config21.mp4',
                   'pure010_20220216_syncSound_77_config21.h5',
                   cameraParams)                    

videos.add_session('2022-02-16', 'chord',
                   'pure010_20220216_syncSound_78_config22.mp4',
                   'pure010_20220216_syncSound_78_config22.h5',
                   cameraParams)

videos.add_session('2022-02-17', '2chords',
                   'pure010_20220217_2Sounds_128_2Sconfig10.mp4',
                   'pure010_20220217_2Sounds_128_2Sconfig10.h5',
                   cameraParams)

videos.add_session('2022-02-17', '2chords',
                   'pure010_20220217_2Sounds_129_2Sconfig10.mp4',
                   'pure010_20220217_2Sounds_129_2Sconfig10.h5',
                   cameraParams)

videos.add_session('2022-02-17', '2chords',
                   'pure010_20220217_2Sounds_130_2Sconfig10.mp4',
                   'pure010_20220217_2Sounds_130_2Sconfig10.h5',
                   cameraParams)