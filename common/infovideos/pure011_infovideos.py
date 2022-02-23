'''
Information about videos.
'''

from jaratoolbox import videoinfo

        
subject = 'pure003'
videos = videoinfo.Videos(subject)
cameraParams = videoinfo.cameraParams['IR_webcam_640x480_30fps_VP9']

videos.add_session('2022-02-15', '2chords',
                   'pure011_20220215_2Sounds_116_2Sconfig9.mp4',
                   'pure011_20220215_2Sounds_116_2Sconfig9.h5',
                   cameraParams) 
                   
videos.add_session('2022-02-15', '2chords',
                   'pure011_20220215_2Sounds_117_2Sconfig9.mp4',
                   'pure011_20220215_2Sounds_117_2Sconfig9.h5',
                   cameraParams)
                   
videos.add_session('2022-02-15', '2chords',
                   'pure011_20220215_2Sounds_118_2Sconfig9.mp4',
                   'pure011_20220215_2Sounds_118_2Sconfig9.h5',
                   cameraParams)

videos.add_session('2022-02-16', 'chord',
                   'pure011_20220216_syncSound_73_config20.mp4',
                   'pure011_20220216_syncSound_73_config20.h5',
                   cameraParams)

videos.add_session('2022-02-16', 'chord',
                   'pure011_20220216_syncSound_74_config21.mp4',
                   'pure011_20220216_syncSound_74_config21.h5',
                   cameraParams)                                     

videos.add_session('2022-02-16', 'chord',
                   'pure011_20220216_syncSound_75_config22.mp4',
                   'pure011_20220216_syncSound_75_config22.h5',
                   cameraParams)                    

videos.add_session('2022-02-17', '2chords',
                   'pure011_20220217_2Sounds_131_2Sconfig10.mp4',
                   'pure011_20220217_2Sounds_131_2Sconfig10.h5',
                   cameraParams)

videos.add_session('2022-02-17', '2chords',
                   'pure011_20220217_2Sounds_132_2Sconfig10.mp4',
                   'pure011_20220217_2Sounds_132_2Sconfig10.h5',
                   cameraParams)

videos.add_session('2022-02-17', '2chords',
                   'pure011_20220217_2Sounds_133_2Sconfig10.mp4',
                   'pure011_20220217_2Sounds_133_2Sconfig10.h5',
                   cameraParams)