from jaratoolbox import videoinfo

subject = 'feat007'
videos = videoinfo.Videos(subject)
cameraParams = videoinfo.cameraParams['IR_webcam_640x480_30fps_VP9']

# Session parameters: date, sessionType, videoFile, behavFile, cameraParams

# 2022-03-10

videos.add_session('2022-03-10', 'AM',
                   'feat007_am_tuning_curve_20220308_01.mkv',
                   'feat007_am_tuning_curve_20220308a.h5', cameraParams) 


videos.add_session('2022-03-10', 'pureTones',
                   'feat007_am_tuning_curve_20220308_02.mkv',
                   'feat007_am_tuning_curve_20220308b.h5', cameraParams) 

videos.add_session('2022-03-10', 'FTVOTBorders',
                   'feat007_2afc_speech_20220308_01.mkv',
                   'feat007_2afc_speech_20220308a.h5', cameraParams) 

