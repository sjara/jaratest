import numpy as np
import pandas as pd
from jaratoolbox import celldatabase
from matplotlib import pyplot as plt

databaseFn = '/tmp/database_with_pulse_responses.h5'
databaseNBQXFn = '/tmp/nbqx_database_with_pulse_responses.h5'

database = celldatabase.load_hdf(databaseFn)
databaseNBQX = celldatabase.load_hdf(databaseNBQXFn)

def jitter(arr, frac):
    jitter = (np.random.random(len(arr))-0.5)*2*frac
    jitteredArr = arr + jitter
    return jitteredArr


plt.clf()
fig = plt.gcf()
# ax = fig.add_subplot(111, projection='3d')
ax0 = fig.add_subplot(121)
ax1 = fig.add_subplot(122)
axes = [ax0, ax1]
for ax in axes:
    ax.hold(1)
# lasercells = database.query('isiViolations<0.02 and spikeShapeQuality>2 and autoTagged==1')
# allcells = database.query('isiViolations<0.02 and spikeShapeQuality>2 and summaryPulsePval<0.05')

#Accept as tagged only cells with latency less than 10ms
CASE=0

if CASE==0:
    latcells = database.query('summaryPulseLatency>0')
    nonlasercells = latcells.query("isiViolations<0.02 and spikeShapeQuality>2 and autoTagged==0 and summaryPulsePval<0.05 and nSpikes>2000 and subject!='pinp018'")
    lasercells = latcells.query('isiViolations<0.02 and spikeShapeQuality>2 and autoTagged==1 and summaryPulsePval<0.05')
    latcellsNBQX = databaseNBQX.query('summaryPulseLatency>0')
    nbqxTagged = latcellsNBQX.query('isiViolations<0.02 and spikeShapeQuality>2 and summaryPulsePval<0.05 and summarySurvivedNBQX==1')
    nbqxNontagged = latcellsNBQX.query('isiViolations<0.02 and spikeShapeQuality>2 and summaryPulsePval<0.05 and summarySurvivedNBQX==0 and autoTagged==0')


elif CASE==1:
    latcells = database.query('summaryPulseLatency>0')
    untaggedcells = latcells.query("isiViolations<0.02 and spikeShapeQuality>2 and autoTagged==0 and summaryPulsePval<0.05 and nSpikes>2000 and subject!='pinp018'")
    longlasercells = latcells.query('isiViolations<0.02 and spikeShapeQuality>2 and autoTagged==1 and summaryPulsePval<0.05 and summaryPulseLatency>=0.01')
    nonlasercells = pd.concat([untaggedcells, longlasercells])
    # lasercells = database.query('isiViolations<0.02 and spikeShapeQuality>2 and autoTagged==1 and pulsePval<0.05 and summaryTrainResponses>=3')
    # lasercells = latcells.query('isiViolations<0.02 and spikeShapeQuality>2 and autoTagged==1 and summaryPulsePval<0.05')
    lasercells = latcells.query('isiViolations<0.02 and spikeShapeQuality>2 and autoTagged==1 and summaryPulsePval<0.05 and summaryPulseLatency<0.01')
    latcellsNBQX = databaseNBQX.query('summaryPulseLatency>0')
    nbqxTagged = latcellsNBQX.query('isiViolations<0.02 and spikeShapeQuality>2 and summaryPulsePval<0.05 and summarySurvivedNBQX==1')
    nbqxNontagged = latcellsNBQX.query('isiViolations<0.02 and spikeShapeQuality>2 and summaryPulsePval<0.05 and summarySurvivedNBQX==0 and autoTagged==0')

elif CASE==2:
    #Don't limit to neurons with significant pulse pvals
    latcells = database.query('summaryPulseLatency>0')
    nonlasercells = latcells.query("isiViolations<0.02 and spikeShapeQuality>2 and autoTagged==0 and nSpikes>2000 and subject!='pinp018'")
    lasercells = latcells.query('isiViolations<0.02 and spikeShapeQuality>2 and autoTagged==1 and summaryPulsePval<0.05')
    latcellsNBQX = databaseNBQX.query('summaryPulseLatency>0')
    nbqxTagged = latcellsNBQX.query('isiViolations<0.02 and spikeShapeQuality>2 and summaryPulsePval<0.05 and summarySurvivedNBQX==1')
    nbqxNontagged = latcellsNBQX.query('isiViolations<0.02 and spikeShapeQuality>2 and summarySurvivedNBQX==0 and autoTagged==0')

# nonlasercells = database.query('isiViolations<0.02 and spikeShapeQuality>2 and autoTagged==0 and pulsePval<0.05')
# lasercells = database.query('isiViolations<0.02 and spkeShapeQuality>2 and autoTagged==1 and pulsePval<0.05')

# laserlatencies = lasercells['trainLatency'].values
# nonlaserlatencies = nonlasercells['trainLatency'].values

# laserreliability = lasercells['trainReliability'].values
# nonlaserreliability = nonlasercells['trainReliability'].values

# laserpulseZ = lasercells['pulseZscore'].values
# nonlaserpulseZ = nonlasercells['pulseZscore'].values

# laserNum = lasercells['numSignificantTrainResponses'].values
# nonlaserNum = nonlasercells['numSignificantTrainResponses'].values

# plt.plot(nonlaserlatencies, nonlaserNum, nonlaserpulseZ, 'k.')
# plt.plot(nonlaserlatencies, nonlaserNum, nonlaserreliability, 'k.')

# plt.plot(allcells['summaryTrainLatency'].values, allcells['summaryTrainResponses'].values, 'k.')
ms = 8
jitterFrac = 0.15

latencyToPlot = 'summaryPulseLatency'
# latencyToPlot = 'summaryPulsePval'
# numResponsesToPlot = 'numSignificantTrainResponses'
numResponsesToPlot = 'summaryTrainResponses'

ax0.plot(nonlasercells[latencyToPlot].values, jitter(nonlasercells[numResponsesToPlot].values, jitterFrac), 'k.', ms=ms)
ax0.plot(lasercells[latencyToPlot].values, jitter(lasercells[numResponsesToPlot].values, jitterFrac), 'c.', ms=ms)

# ax0.plot(nonlasercells[latencyToPlot].values, nonlasercells['summaryTrainLatency'].values, 'k.', ms=ms)
# ax0.plot(lasercells[latencyToPlot].values, lasercells['summaryTrainLatency'].values, 'c.', ms=ms)



ax1.plot(nbqxTagged[latencyToPlot].values, jitter(nbqxTagged[numResponsesToPlot].values, jitterFrac), 'g.', ms=ms)
ax1.plot(nbqxNontagged[latencyToPlot].values, jitter(nbqxNontagged[numResponsesToPlot].values, jitterFrac), 'r.', ms=ms)

# ax1.plot(nbqxTagged[latencyToPlot].values, nbqxTagged['summaryTrainLatency'].values, 'g.', ms=ms)
# ax1.plot(nbqxNontagged[latencyToPlot].values, nbqxNontagged['summaryTrainLatency'].values, 'r.', ms=ms)


for ax in axes:
    ax.set_xlabel('Latency of response to laser pulse (s)')
    # ax.set_xlabel('Pulse p-value')
    ax.set_xlim([0, 0.05])
    ax.set_ylabel('Significant train responses')
# ax.set_zlabel('pulse Z score')
# plt.plot(laserlatencies, laserNum, laserpulseZ, 'b.')
# plt.plot(laserlatencies, laserNum, laserreliability, 'b.')
# plt.plot(laserlatencies, laserNum, 'b.')
# ax.axvline(x=0.01, color='0.5')

# plt.plot(nonlaserlatencies, nonlaserNum, 'k.')
# ax.set_xlabel('latency')
# ax.set_xlim([0, 0.1])
# ax.set_ylabel('num significant train responses')
# # ax.set_zlabel('pulse Z score')
# # plt.plot(laserlatencies, laserNum, laserpulseZ, 'b.')
# # plt.plot(laserlatencies, laserNum, laserreliability, 'b.')
# plt.plot(laserlatencies, laserNum, 'b.')
# ax.axvline(x=0.01, color='r')
plt.show()
