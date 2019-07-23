import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis
from jaratoolbox import ephyscore
from jaratest.nick.reports import pinp_report
from collections import Counter
from scipy import stats
from scipy import signal
import pandas as pd
import figparams
reload(figparams)
reload(pinp_report)

dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS.h5')

db = pd.read_hdf(dbPath, key='dataframe')
# db = db.query("subject=='pinp015'")
# goodLaser = db.query('pulsePval<0.05 and pulseZscore>0 and trainRatio>0.8')
# goodLaser = db[db['taggedCond']==0]
goodISI = db.query('isiViolations<0.02 or modifiedISI<0.02')
goodShape = goodISI.query('spikeShapeQuality > 2')
# goodLaser = goodShape.query('autoTagged==1')
goodNoise = goodShape.query('noisePval<0.05')

reportDir = '/tmp/20180417_NoiseCells'

for indRow, dbRow in goodNoise.iterrows():

    try:
        subject = dbRow['subject']
        date = dbRow['date']
        depth = dbRow['depth']
        tetrode = dbRow['tetrode']
        cluster = int(dbRow['cluster'])
        brainArea = dbRow['brainArea']
        cellName = "{}_{}_{}_TT{}c{}".format(subject, date, depth, tetrode, cluster)
        print "Plotting report for {}".format(cellName)

        plt.clf()
        pinp_report.plot_pinp_report(dbRow, useModifiedClusters=True)
        figsize = (9, 11)
        plt.gcf().set_size_inches(figsize)
        fullDir = os.path.join(reportDir, brainArea)
        if not os.path.exists(fullDir):
            os.mkdir(fullDir)
        fullName = os.path.join(fullDir, cellName)
        plt.savefig(fullName,format='png')
    except:
        continue



