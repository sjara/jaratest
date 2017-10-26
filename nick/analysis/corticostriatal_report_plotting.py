import pandas
from jaratest.nick.reports import pinp_report
reload(pinp_report)
from jaratest.nick.reports import str_report
import os
from matplotlib import pyplot as plt

# dbFn = '/home/nick/data/database/corticostriatal_master_2017-05-29_15-47-34.h5'
dbFn = '/home/nick/data/database/corticostriatal_pinp019_2017-06-01_12-53-18.h5'
db = pandas.read_hdf(dbFn, 'database')

#Plotting: Bad ISI (>0.02), Bad Waveforms (ISI < 0.02, shapeQual < 2)
#Non-sound-responsive (ISI < 0.02, shapeQual > 2, noisePval > 0.05)
#Sound responsive (ISI < 0.02, shapeQual > 2, noisePval < 0.05)

#
failures = []

baseDir = '/home/nick/data/reports/nick/thalamostr'
badisi = db.query('isiViolations>0.02')
for indCell, cell in badisi.iterrows():
    if indCell>738:
        try:
            pinp_report.plot_pinp_report(cell, os.path.join(baseDir, 'badisi'))
            print "bad isi cell {}".format(indCell)
        except:
            failures.append(indCell)
            continue


badwave = db.query('isiViolations<0.02 and shapeQuality<2')
for indCell, cell in badwave.iterrows():
    try:
        pinp_report.plot_pinp_report(cell, os.path.join(baseDir, 'badwave'))
        print "bad waveform cell {}".format(indCell)
    except:
        failures.append(indCell)
        continue

nonresponsive = db.query('isiViolations<0.02 and shapeQuality>2 and noisePval>0.05')
for indCell, cell in nonresponsive.iterrows():
    try:
        pinp_report.plot_pinp_report(cell, os.path.join(baseDir, 'nonresponsive'))
        print "nonresponsive cell {}".format(indCell)
    except:
        failures.append(indCell)
        continue

responsive = db.query('isiViolations<0.02 and shapeQuality>2 and noisePval<0.05')
for indCell, cell in responsive.iterrows():
    try:
        pinp_report.plot_pinp_report(cell, os.path.join(baseDir, 'responsive'))
        print "sound responsive cell {}".format(indCell)
    except:
        failures.append(indCell)
        continue
