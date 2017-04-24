from jaratoolbox import celldatabase
from jaratoolbox import spikesorting
from jaratest.nick.stats import eventresponse
from jaratest.nick.stats import am_funcs
from numpy import inf
import pandas
from jaratest.nick.analysis.pinp_report import *
from matplotlib import pyplot as plt

from jaratest.nick.stats import tuningfuncs
from jaratest.nick.database import dataloader_v2 as dataloader

inforec = '/home/nick/src/jaratest/nick/inforecordings/pinp017/pinp017_inforec.py'

# ci = spikesorting.ClusterInforec(inforec)

# ci.cluster_all_experiments()

db = celldatabase.generate_cell_database(inforec)

allShapeQuality = np.empty(len(db))
for indCell, cell in db.iterrows():
    peakAmplitudes = cell['clusterPeakAmplitudes']
    spikeShapeSD = cell['clusterSpikeSD']
    shapeQuality = abs(peakAmplitudes[1]/spikeShapeSD.mean())
    allShapeQuality[indCell] = shapeQuality
allShapeQuality[allShapeQuality==inf]=0
db['shapeQuality'] = allShapeQuality

#Noise response, new version
noiseZscore = np.empty(len(db))
noisePval = np.empty(len(db))
baseRange = [-0.2,0]
responseRange = [0, 0.2]
for indCell, cell in db.iterrows():
    zScore, pVal = eventresponse.event_response_score(cell, 'noiseburst',
                                                      responseRange=responseRange,
                                                      baseRange=baseRange)
    noiseZscore[indCell] = zScore
    noisePval[indCell] = pVal
db['noiseZscore'] = noiseZscore
db['noisePval'] = noisePval

#Laser pulse response
pulseZscore = np.empty(len(db))
pulsePval = np.empty(len(db))
for indCell, cell in db.iterrows():
    zScore, pVal = eventresponse.event_response_score(cell, 'laserpulse')
    pulseZscore[indCell] = zScore
    pulsePval[indCell] = pVal
db['pulseZscore'] = pulseZscore
db['pulsePval'] = pulsePval

#Laser train response
trainRatio = np.empty(len(db))
for indCell, cell in db.iterrows():
    ratio = eventresponse.train_response_ratio(cell, 'lasertrain')
    trainRatio[indCell] = ratio
    print ratio
db['trainRatio'] = trainRatio

#AM stats
amRval = np.empty(len(db))
highestSync = np.empty(len(db))
for indCell, cell in db.iterrows():
    r_val = am_funcs.am_dependence(cell)
    amRval[indCell] = r_val
    hs = am_funcs.highest_significant_sync(cell)
    highestSync[indCell] = hs
db['amRval'] = amRval
db['highestSync'] = highestSync


soundResponsive = db.query('isiViolations<0.02 and shapeQuality>2 and noisePval<0.05')
soundLaserResponsive = soundResponsive.query('pulsePval<0.05 and trainRatio>0.8')

q10s = []
ixs = []
tcType = 'tc'
for index, cell in soundResponsive.iterrows():
    loader = dataloader.DataLoader(cell['subject'])
    tuningindex = cell['sessiontype'].index(tcType)
    bdata = loader.get_session_behavior(cell['behavior'][tuningindex])
    possibleFreq = np.unique(bdata['currentFreq'])
    possibleInten = np.unique(bdata['currentIntensity'])
    zvalArray = tuningfuncs.tuning_curve_response(cell)
    tuner = tuningfuncs.TuningAnalysis(np.flipud(zvalArray), freqLabs = possibleFreq, intenLabs = possibleInten[::-1])
    button = True
    while button:
        button = plt.waitforbuttonpress()
    button = True
    while button:
        button = plt.waitforbuttonpress()
    button = True
    while button:
        button = plt.waitforbuttonpress()
    button = True
    while button:
        button = plt.waitforbuttonpress()
    q10 = tuner.Q10
    db.set_value(index, 'Q10', tuner.Q10)
    db.set_value(index, 'bestFreq', tuner.bestFreq)
    db.set_value(index, 'highFreq', tuner.highFreq)
    db.set_value(index, 'lowFreq', tuner.lowFreq)
    db.set_value(index, 'threshold', tuner.threshold)

db.to_hdf('/home/nick/data/database/pinp017/pinp017_database.h5', 'database')
