from jaratoolbox import videoinfo

subject = 'feat008'
videos = videoinfo.Videos(subject)
cameraParams = videoinfo.cameraParams['IR_webcam_640x480_30fps_VP9']

# Session parameters: date, sessionType, videoFile, behavFile, cameraParams

# 2022-03-23

videos.add_session('2022-03-23', 'AM',
                   'feat008_am_tuning_curve_20220323_01.mkv',
                   'feat008_am_tuning_curve_20220323a.h5', cameraParams) 


videos.add_session('2022-03-23', 'pureTones',
                   'feat008_am_tuning_curve_20220323_02.mkv',
                   'feat008_am_tuning_curve_20220323b.h5', cameraParams) 

videos.add_session('2022-03-23', 'FTVOTBorders',
                   'feat008_2afc_speech_20220323_01.mkv',
                   'feat008_2afc_speech_20220323a.h5', cameraParams) 


# 2022-03-24

videos.add_session('2022-03-24', 'AM',
                   'feat008_am_tuning_curve_20220324_01.mkv',
                   'feat008_am_tuning_curve_20220324a.h5', cameraParams) 


videos.add_session('2022-03-24', 'pureTones',
                   'feat008_am_tuning_curve_20220324_02.mkv',
                   'feat008_am_tuning_curve_20220324b.h5', cameraParams) 

videos.add_session('2022-03-24', 'FTVOTBorders',
                   'feat008_2afc_speech_20220324_01.mkv',
                   'feat008_2afc_speech_20220324a.h5', cameraParams) 
                   
# 2022-03-25

videos.add_session('2022-03-25', 'AM',
                   'feat008_am_tuning_curve_20220325_01.mkv',
                   'feat008_am_tuning_curve_20220325a.h5', cameraParams) 


videos.add_session('2022-03-25', 'pureTones',
                   'feat008_am_tuning_curve_20220325_02.mkv',
                   'feat008_am_tuning_curve_20220325b.h5', cameraParams) 

videos.add_session('2022-03-25', 'FTVOTBorders',
                   'feat008_2afc_speech_20220325_01.mkv',
                   'feat008_2afc_speech_20220325a.h5', cameraParams) 
