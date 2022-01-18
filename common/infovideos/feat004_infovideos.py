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



                   

