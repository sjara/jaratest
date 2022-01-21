from jaratoolbox import videoinfo

subject = 'feat004'
videos = videoinfo.Videos(subject)
cameraParams = videoinfo.cameraParams['IR_webcam_640x480_30fps_VP9']

# Session parameters: date, sessionType, videoFile, behavFile, cameraParams

videos.add_session('2022-01-11', 'VOT',
                   'feat004_2afc_speech_20220111_01.mkv',
                   'feat004_2afc_speech_20220111a.h5',
                   cameraParams) 
                   
videos.add_session('2022-01-11', 'FT',
                   'feat004_2afc_speech_20220111_02.mkv',
                   'feat004_2afc_speech_20220111b.h5',
                   cameraParams) 


# 2022-01-19
videos.add_session('2022-01-19', 'pureTones',
                   'feat004_am_tuning_curve_20220119_01.mkv',
                   'feat004_am_tuning_curve_20220119a.h5',
                   cameraParams)                    

videos.add_session('2022-01-19', 'AM',
                   'feat004_am_tuning_curve_20220119_02.mkv',
                   'feat004_am_tuning_curve_20220119b.h5',
                   cameraParams) 
                   
videos.add_session('2022-01-19', 'FT',
                   'feat004_2afc_speech_20220119_01.mkv',
                   'feat004_2afc_speech_20220119a.h5',
                   cameraParams) 
                   
                   
videos.add_session('2022-01-19', 'VOT',
                   'feat004_2afc_speech_20220119_02.mkv',
                   'feat004_2afc_speech_20220119b.h5',
                   cameraParams) 
                   
# 2022-01-21
videos.add_session('2022-01-21', 'pureTones',
                   'feat004_am_tuning_curve_20220121_01.mkv',
                   'feat004_am_tuning_curve_20220121a.h5',
                   cameraParams)                    

videos.add_session('2022-01-21', 'AM',
                   'feat004_am_tuning_curve_20220121_02.mkv',
                   'feat004_am_tuning_curve_20220121b.h5',
                   cameraParams) 
                   
videos.add_session('2022-01-21', 'FTVOTBorders',
                   'feat004_2afc_speech_20220121_01.mkv',
                   'feat004_2afc_speech_20220121a.h5',
                   cameraParams) 
