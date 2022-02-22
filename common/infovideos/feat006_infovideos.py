from jaratoolbox import videoinfo

subject = 'feat006'
videos = videoinfo.Videos(subject)
cameraParams = videoinfo.cameraParams['IR_webcam_640x480_30fps_VP9']

# Session parameters: date, sessionType, videoFile, behavFile, cameraParams

# 2022-02-21

videos.add_session('2022-02-21', 'AM',
                   'feat006_am_tuning_curve_20220221_01.mkv',
                   'feat006_am_tuning_curve_20220221a.h5',
                   cameraParams) 

videos.add_session('2022-02-21', 'pureTones',
                   'feat006_am_tuning_curve_20220221_02.mkv',
                   'feat006_am_tuning_curve_20220221b.h5',
                   cameraParams) 
                   
videos.add_session('2022-02-21', 'FTVOTBorders',
                   'feat006_2afc_speech_20220221_01.mkv',
                   'feat006_2afc_speech_20220221a.h5',
                   cameraParams) 

#2022-02-22
videos.add_session('2022-02-22', 'AM',
                   'feat006_am_tuning_curve_20220222_01.mkv',
                   'feat006_am_tuning_curve_20220222a.h5',
                   cameraParams) 

videos.add_session('2022-02-22', 'pureTones',
                   'feat006_am_tuning_curve_20220222_02.mkv',
                   'feat006_am_tuning_curve_20220222b.h5',
                   cameraParams) 
                   
videos.add_session('2022-02-22', 'FTVOTBorders',
                   'feat006_2afc_speech_20220222_01.mkv',
                   'feat006_2afc_speech_20220222a.h5',
                   cameraParams) 
          
 
