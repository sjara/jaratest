#rsync -a --progress --exclude '*.continuous' jarauser@jaraphys2:~/data/ephys/adap020/ ~/data/ephys/adap020/
#rsync -a --progress jarauser@jararig2:/data/behavior/adap020/ ~/data/behavior/adap020/

#time rsync -a --progress ~/data/ephys/adap020* /media/billywalker/7ac73554-c9d6-4274-9780-cf002cb28288/data/ephys/
#python adap020_clustering.py
#rm ~/data/ephys/adap020/multisession_*/*.fet.*
#time rsync -a --progress ~/data/ephys/adap020* /media/billywalker/7ac73554-c9d6-4274-9780-cf002cb28288/data/ephys/

#python test055_clustering.py
#rm ~/data/ephys/test055/multisession_*/*.fet.*

#python test053_clustering.py
#rm ~/data/ephys/test053/multisession_*/*.fet.*

#python adap017_clustering.py
#rm ~/data/ephys/adap017/multisession_*/*.fet.*
#time rsync -a --progress ~/data/ephys/adap017* /media/billywalker/7ac73554-c9d6-4274-9780-cf002cb28288/data/ephys/


#python adap015_clustering.py
#rm ~/data/ephys/adap015/multisession_*/*.fet.*

#python adap013_clustering.py
#rm ~/data/ephys/adap013/multisession_*/*.fet.*

#python test017_clustering.py
#rm ~/data/ephys/test017/*_kk/*.fet.*

#python test089_clustering.py
#rm ~/data/ephys/test089/*_kk/*.fet.*


#python addModulationCheckSwitching.py adap020 #must be run before switching report
#python test029_add_ISIViolations.py adap020
#python addMinTrialCheckSwitching.py adap020
#python addMinBehavePerformanceSwitch.py adap020
#python add_sound_response_stat.py adap020
#python test029_add_ISIViolations.py adap020
#time rsync -a --progress ~/data/ephys/adap020_pro* /media/billywalker/7ac73554-c9d6-4274-9780-cf002cb28288/data/ephys/
#python switch_tuning_report.py adap020
#python test038_write_maxZ_movement_response_stat.py adap020

#python addModulationCheckPsyCurve.py adap017 #must be run before switching report
#python test029_add_ISIViolations.py adap017
#python add_sound_response_stat.py adap017
#time rsync -a --progress ~/data/ephys/adap017* /media/billywalker/7ac73554-c9d6-4274-9780-cf002cb28288/data/ephys/

#python addModulationCheckPsyCurve.py adap013 #must be run before switching report
#python test029_add_ISIViolations.py adap013
#python add_sound_response_stat.py adap013
#time rsync -a --progress ~/data/ephys/adap013* /media/billywalker/7ac73554-c9d6-4274-9780-cf002cb28288/data/ephys/

#python addModulationCheckPsyCurve.py adap015 #must be run before switching report
#python test029_add_ISIViolations.py adap015
#python add_sound_response_stat.py adap015
#time rsync -a --progress ~/data/ephys/adap015* /media/billywalker/7ac73554-c9d6-4274-9780-cf002cb28288/data/ephys/


#python addModulationCheckSwitching.py test017 #must be run before switching report
#python test029_add_ISIViolations.py test017
#python addMinTrialCheckSwitching.py test017
#python addMinBehavePerformanceSwitch.py test017
#python add_sound_response_stat.py test017
#python switch_tuning_report.py test017


#python addModulationCheckPsyCurve.py test055 #must be run before switching report
#python test029_add_ISIViolations.py test055
#python add_sound_response_stat.py test055
#time rsync -a --progress ~/data/ephys/test055* /media/billywalker/7ac73554-c9d6-4274-9780-cf002cb28288/data/ephys/


#python addModulationCheckPsyCurve.py test053 #must be run before switching report
#python test029_add_ISIViolations.py test053
#python add_sound_response_stat.py test053
#time rsync -a --progress ~/data/ephys/test053* /media/billywalker/7ac73554-c9d6-4274-9780-cf002cb28288/data/ephys/


#python psycurve_tuning_allFreq_movement_report.py adap017
#python psycurve_tuning_centerfreq_sound_report.py adap017

#python psycurve_tuning_allFreq_movement_report.py adap013
#python psycurve_tuning_centerfreq_sound_report.py adap013

#python psycurve_tuning_allFreq_movement_report.py adap015
#python psycurve_tuning_centerfreq_sound_report.py adap015

python psycurve_tuning_allFreq_movement_report.py test055
#python psycurve_tuning_centerfreq_sound_report.py test055

python psycurve_tuning_allFreq_movement_report.py test053
#python psycurve_tuning_centerfreq_sound_report.py test053

#python switch_tuning_report.py test089
#python switch_tuning_allfreq_report.py test089
#python switch_tuning_block_allfreq_report.py test089
#python switch_tuning_sidein_report.py test089

#python switch_tuning_report.py test059
#python switch_tuning_allfreq_report.py test059
#python switch_tuning_block_allfreq_report.py test059
#python switch_tuning_sidein_report.py test059

#python switch_tuning_report.py test017
#python switch_tuning_allfreq_report.py test017
#python switch_tuning_block_allfreq_report.py test017
#python switch_tuning_sidein_report.py test017

#python switch_tuning_report.py adap020
#python switch_tuning_allfreq_report.py adap020
python switch_tuning_block_allfreq_report.py adap020
python switch_tuning_sidein_report.py adap020
