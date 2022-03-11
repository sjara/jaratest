from jaratoolbox import videoinfo

subject = 'feat007'
videos = videoinfo.Videos(subject)
cameraParams = videoinfo.cameraParams['IR_webcam_640x480_30fps_VP9']

# Session parameters: date, sessionType, videoFile, behavFile, cameraParams

# 2022-03-10

videos.add_session('2022-03-10', 'AM',
                   'feat007_am_tuning_curve_20220310_01.mkv',
                   'feat007_am_tuning_curve_20220310a.h5', cameraParams) 


videos.add_session('2022-03-10', 'pureTones',
                   'feat007_am_tuning_curve_20220310_02.mkv',
                   'feat007_am_tuning_curve_20220310b.h5', cameraParams) 

videos.add_session('2022-03-10', 'FTVOTBorders',
                   'feat007_2afc_speech_20220310_01.mkv',
                   'feat007_2afc_speech_20220310a.h5', cameraParams) 

# 2022-03-11

videos.add_session('2022-03-11', 'AM',
                   'feat007_am_tuning_curve_20220311_01.mkv',
                   'feat007_am_tuning_curve_20220311a.h5', cameraParams) 


videos.add_session('2022-03-11', 'pureTones',
                   'feat007_am_tuning_curve_20220311_02.mkv',
                   'feat007_am_tuning_curve_20220311b.h5', cameraParams) 

videos.add_session('2022-03-11', 'FTVOTBorders',
                   'feat007_2afc_speech_20220311_01.mkv',
                   'feat007_2afc_speech_20220311a.h5', cameraParams) 


