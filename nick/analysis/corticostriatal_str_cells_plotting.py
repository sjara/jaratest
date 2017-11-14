import pandas
from jaratest.nick.reports import pinp_report
reload(pinp_report)
from jaratest.nick.reports import str_report
import os
from matplotlib import pyplot as plt
from jaratest.nick.analysis.corticostriatal_object_oriented import Analysis
import datetime

#TODO: save the db

strobj = Analysis(['pinp020'])
strobj.calculate_shape_quality(dataframe=strobj.db)
strobj.calculate_noiseburst_response(dataframe=strobj.db)
strobj.calculate_am_statistics(dataframe=strobj.db)
strobj.calculate_highest_significant_sync_rate(dataframe=strobj.db)
strobj.calculate_tuning_curve_params(dataframe=strobj.db)

now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
strobj.db.to_hdf('/home/nick/data/database/corticostriatal_striatumcells_{}.h5'.format(now), 'database')

db = strobj.db

#Plotting: Bad ISI (>0.02), Bad Waveforms (ISI < 0.02, shapeQual < 2)
#Non-sound-responsive (ISI < 0.02, shapeQual > 2, noisePval > 0.05)
#Sound responsive (ISI < 0.02, shapeQual > 2, noisePval < 0.05)

#
failures = []

baseDir = '/home/nick/data/reports/nick/thalamostr_striatum'
badisi = db.query('isiViolations>0.02')
for indCell, cell in badisi.iterrows():
    if indCell>738:
        try:
            str_report.plot_str_report(cell, os.path.join(baseDir, 'badisi'))
            print "bad isi cell {}".format(indCell)
        except:
            failures.append(indCell)
            continue


badwave = db.query('isiViolations<0.02 and shapeQuality<2')
for indCell, cell in badwave.iterrows():
    try:
        str_report.plot_str_report(cell, os.path.join(baseDir, 'badwave'))
        print "bad waveform cell {}".format(indCell)
    except:
        failures.append(indCell)
        continue

nonresponsive = db.query('isiViolations<0.02 and shapeQuality>2 and noisePval>0.05')
for indCell, cell in nonresponsive.iterrows():
    try:
        str_report.plot_str_report(cell, os.path.join(baseDir, 'nonresponsive'))
        print "nonresponsive cell {}".format(indCell)
    except:
        failures.append(indCell)
        continue

responsive = db.query('isiViolations<0.02 and shapeQuality>2 and noisePval<0.05')
for indCell, cell in responsive.iterrows():
    try:
        str_report.plot_str_report(cell, os.path.join(baseDir, 'responsive'))
        print "sound responsive cell {}".format(indCell)
    except:
        failures.append(indCell)
        continue
