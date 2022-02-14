from jaratoolbox import videoinfo

subject = 'feat005'
videos = videoinfo.Videos(subject)
cameraParams = videoinfo.cameraParams['IR_webcam_640x480_30fps_VP9']

# Session parameters: date, sessionType, videoFile, behavFile, cameraParams

# 2022-02-07
#videos.add_session('2022-02-07', 'pureTones',
#                   'feat005_am_tuning_curve_20220207_01.mkv',
#                   'feat005_am_tuning_curve_20220207a.h5',
#                   cameraParams)                  

videos.add_session('2022-02-07', 'AM',
                   'feat005_am_tuning_curve_20220207_02.mkv',
                   'feat005_am_tuning_curve_20220207b.h5',
                   cameraParams) 
                   
videos.add_session('2022-02-07', 'FTVOTBorders',
                   'feat005_2afc_speech_20220207_01.mkv',
                   'feat005_2afc_speech_20220207a.h5',
                   cameraParams) 
                   
videos.add_session('2022-02-07', 'pureTones',
                   'feat005_am_tuning_curve_20220207_03.mkv',
                   'feat005_am_tuning_curve_20220207c.h5',
                   cameraParams)   
                   
# 2022-02-08
videos.add_session('2022-02-08', 'pureTones',
                   'feat005_am_tuning_curve_20220208_01.mkv',
                   'feat005_am_tuning_curve_20220208a.h5',
                   cameraParams)                   

videos.add_session('2022-02-08', 'AM',
                   'feat005_am_tuning_curve_20220208_02.mkv',
                   'feat005_am_tuning_curve_20220208b.h5',
                   cameraParams) 
                  
videos.add_session('2022-02-08', 'FTVOTBorders',
                   'feat005_2afc_speech_20220208_01.mkv',
                   'feat005_2afc_speech_20220208a.h5',
                   cameraParams) 
                   
# 2022-02-11
videos.add_session('2022-02-11', 'pureTones',
                   'feat005_am_tuning_curve_20220211_01.mkv',
                   'feat005_am_tuning_curve_20220211a.h5',
                   cameraParams)                  

videos.add_session('2022-02-11', 'AM',
                   'feat005_am_tuning_curve_20220211_02.mkv',
                   'feat005_am_tuning_curve_20220211b.h5',
                   cameraParams) 
                  
videos.add_session('2022-02-11', 'FTVOTBorders',
                   'feat005_2afc_speech_20220211_01.mkv',
                   'feat005_2afc_speech_20220211a.h5',
                   cameraParams) 
                   
# 2022-02-14
videos.add_session('2022-02-14', 'pureTones',
                   'feat005_am_tuning_curve_20220214_01.mkv',
                   'feat005_am_tuning_curve_20220214a.h5',
                   cameraParams)                 

videos.add_session('2022-02-14', 'AM',
                   'feat005_am_tuning_curve_20220214_02.mkv',
                   'feat005_am_tuning_curve_20220214b.h5',
                   cameraParams) 
                  
videos.add_session('2022-02-14', 'FTVOTBorders',
                   'feat005_2afc_speech_20220214_01.mkv',
                   'feat005_2afc_speech_20220214a.h5',
                   cameraParams) 
