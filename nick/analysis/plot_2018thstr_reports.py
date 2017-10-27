import os
import pandas as pd
from jaratest.nick.reports import pinp_report

dbPath = '/home/nick/src/jaratest/common/2018thstr/celldatabase.h5'
db = pd.read_hdf(dbPath, key='dataframe')

soundResponsive = db.query('isiViolations<0.02 and shapeQuality>2 and noisePval<0.05')
soundLaserResponsive = soundResponsive.query('pulsePval<0.05 and trainRatio>0.8')

testSet = soundResponsive[:5]

def already_plotted(cell, path):
    figName = '{}_{}_{}um_TT{}c{}.png'.format(cell['subject'],
                                              cell['date'],
                                              int(cell['depth']),
                                              int(cell['tetrode']),
                                              int(cell['cluster']))
    fullpath = os.path.join(path, figName)
    return os.path.exists(fullpath)

figPath = '/home/nick/data/reports/nick/2018thstr_thalamus'
for indCell, cell in soundResponsive.groupby('brainarea').get_group('rightThal').iterrows():
    if not already_plotted(cell, figPath):
        pinp_report.plot_pinp_report(cell, figPath)

for indCell, cell in soundResponsive.groupby('brainarea').get_group('rightThalamus').iterrows():
    if not already_plotted(cell, figPath):
        pinp_report.plot_pinp_report(cell, figPath)

figPath = '/home/nick/data/reports/nick/2018thstr_cortex'
for indCell, cell in soundResponsive.groupby('brainarea').get_group('rightAC').iterrows():
    if not already_plotted(cell, figPath):
        pinp_report.plot_pinp_report(cell, figPath)

# figPath = '/home/nick/data/reports/nick/2018thstr_striatum'
# for indCell, cell in soundResponsive.groupby('brainarea').get_group('rightAstr').iterrows():
#     pinp_report.plot_pinp_report(cell, figPath)
