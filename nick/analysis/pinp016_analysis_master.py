from jaratoolbox import celldatabase
import pandas
import subprocess
from jaratest.nick.analysis import pinp_report
reload(pinp_report)
from jaratest.nick.analysis.pinp_report import *

pinp016db = celldatabase.generate_cell_database('/home/nick/src/jaratest/nick/inforecordings/pinp016/pinp016_inforec.py')

pinp016db.to_hdf('/home/nick/data/database/pinp016/pinp016_database.h5', 'database')

#Then run script for waveform analysis, then laser analysis

waveformAnalysis = ['python', '/home/nick/src/jaratest/nick/analysis/pinp016_waveform_analysis.py']
subprocess.call(waveformAnalysis)

laserAnalysis = ['python', '/home/nick/src/jaratest/nick/analysis/pinp016_laser_analysis.py']
subprocess.call(laserAnalysis)

postAnalysisFn = '/home/nick/data/database/pinp016/pinp016_database_shape_laser.h5'
pinp016db = pandas.read_hdf(postAnalysisFn, key='database')

result = pinp016db.query('isiViolations<0.02 and shapeQuality>2 and pulsePval<0.05 and trainRatio>0.8')
# result = pinp016db.query('isiViolations<0.02')

fig_path = '/home/nick/data/database/pinp016/reports_isi_shape_laser_train/'
for indCell, cell in result.iterrows():
    plot_pinp_report(cell, fig_path)

