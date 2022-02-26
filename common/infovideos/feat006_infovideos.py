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
          
#2022-02-24
videos.add_session('2022-02-24', 'AM',
                   'feat006_am_tuning_curve_20220224_01.mkv',
                   'feat006_am_tuning_curve_20220224a.h5',
                   cameraParams) 

videos.add_session('2022-02-24', 'pureTones',
                   'feat006_am_tuning_curve_20220224_02.mkv',
                   'feat006_am_tuning_curve_20220224b.h5',
                   cameraParams) 
                   
videos.add_session('2022-02-24', 'FTVOTBorders',
                   'feat006_2afc_speech_20220224_01.mkv',
                   'feat006_2afc_speech_20220224a.h5',
                   cameraParams) 
                   
                   
#2022-02-25
videos.add_session('2022-02-25', 'AM',
                   'feat006_am_tuning_curve_20220225_01.mkv',
                   'feat006_am_tuning_curve_20220225a.h5',
                   cameraParams) 

videos.add_session('2022-02-25', 'pureTones',
                   'feat006_am_tuning_curve_20220225_02.mkv',
                   'feat006_am_tuning_curve_20220225b.h5',
                   cameraParams) 
                   
videos.add_session('2022-02-25', 'FTVOTBorders',
                   'feat006_2afc_speech_20220225_01.mkv',
                   'feat006_2afc_speech_20220225a.h5',
                   cameraParams) 
                   
#2022-02-26
videos.add_session('2022-02-26', 'AM',
                   'feat006_am_tuning_curve_20220226_01.mkv',
                   'feat006_am_tuning_curve_20220226a.h5',
                   cameraParams) 

videos.add_session('2022-02-26', 'pureTones',
                   'feat006_am_tuning_curve_20220226_02.mkv',
                   'feat006_am_tuning_curve_20220226b.h5',
                   cameraParams) 
                   
videos.add_session('2022-02-26', 'FTVOTBorders',
                   'feat006_2afc_speech_20220226_01.mkv',
                   'feat006_2afc_speech_20220226a.h5',
                   cameraParams)                    
