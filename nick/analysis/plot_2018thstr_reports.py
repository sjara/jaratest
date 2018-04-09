import os
import numpy as np
import pandas as pd
from jaratoolbox import settings
from jaratest.nick.reports import pinp_report
reload(pinp_report)

STUDY_NAME = '2018thstr'

dbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, 'celldatabase.h5')
db = pd.read_hdf(dbPath, key='dataframe')

CASE=2

if CASE==0:
    #Plot cells in the frequency BW summary dataset
    figGroup = '2018thstr_freqBW'

    goodLaser = db.query('isiViolations<0.02 and spikeShapeQuality>2 and pulsePval<0.05 and pulseZscore>0 and trainRatio>0.8')
    goodFit = goodLaser.query('rsquaredFit > 0.08')

    #Calculate the midpoint of the gaussian fit
    goodFit['fitMidPoint'] = np.sqrt(goodFit['upperFreq']*goodFit['lowerFreq'])
    goodFitToUse = goodFit.query('fitMidPoint<32000')

    #Which dataframe to use
    # dataframe = goodFit
    dbToUse = goodFitToUse

elif CASE==1:
    #plot cells in the AM highest sync summary dataset
    figGroup = '2018thstr_AM'
    goodLaser = db.query('isiViolations<0.02 and spikeShapeQuality>2 and pulsePval<0.05 and pulseZscore>0 and trainRatio>0.8')
    hsFeatureName = 'highestSyncCorrected'
    dbToUse = goodLaser[pd.notnull(goodLaser[hsFeatureName])]


elif CASE==2:
    #plot cells in the Far untagged group
    figGroup = '2018thstr_FarUntagged'
    goodLaser = db.query('isiViolations<0.02 and spikeShapeQuality>2 and farUntagged==True')
    hsFeatureName = 'highestSyncCorrected'
    dbToUse = goodLaser[pd.notnull(goodLaser[hsFeatureName])]

def already_plotted(cell, path):
    figName = '{}_{}_{}um_TT{}c{}.png'.format(cell['subject'],
                                              cell['date'],
                                              int(cell['depth']),
                                              int(cell['tetrode']),
                                              int(cell['cluster']))
    fullpath = os.path.join(path, figName)
    return os.path.exists(fullpath)

REPLOT = True
subfolder = '20180321_reports'
figPath = '/home/nick/data/reports/nick/{}/{}/thalamus'.format(subfolder, figGroup)
if not os.path.exists(figPath):
    os.makedirs(figPath)
for indCell, cell in dbToUse.groupby('brainArea').get_group('rightThal').iterrows():
    if REPLOT:
        pinp_report.plot_pinp_report(cell, figPath)
    else:
        if not already_plotted(cell, figPath):
            pinp_report.plot_pinp_report(cell, figPath)


# for indCell, cell in dbToUse.groupby('brainArea').get_group('rightThalamus').iterrows():
#     if REPLOT:
#         pinp_report.plot_pinp_report(cell, figPath)
#     else:
#         if not already_plotted(cell, figPath):
#             pinp_report.plot_pinp_report(cell, figPath)

figPath = '/home/nick/data/reports/nick/{}/{}/cortex'.format(subfolder, figGroup)
if not os.path.exists(figPath):
    os.makedirs(figPath)
for indCell, cell in dbToUse.groupby('brainArea').get_group('rightAC').iterrows():
    if REPLOT:
        pinp_report.plot_pinp_report(cell, figPath)
    else:
        if not already_plotted(cell, figPath):
            pinp_report.plot_pinp_report(cell, figPath)

# figPath = '/home/nick/data/reports/nick/2018thstr_striatum'
# for indCell, cell in dbToUse.groupby('brainarea').get_group('rightAstr').iterrows():
#     pinp_report.plot_pinp_report(cell, figPath)
