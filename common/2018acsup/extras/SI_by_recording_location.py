import numpy as np
import scipy.stats
import matplotlib.pyplot as plt

from jaratoolbox import celldatabase

FONTSIZE = 14

db = celldatabase.load_hdf('/mnt/jarahubdata/figuresdata/2018acsup/photoidentification_cells.h5')
bestCells = db.query('isiViolations<0.02 or modifiedISI<0.02')
bestCells = bestCells.query('spikeShapeQuality>2.5 and tuningFitR2>0.1 and octavesFromPrefFreq<0.3 and sustainedSoundResponsePVal<0.05')

LASER_RESPONSE_PVAL = 0.001 #want to be EXTRA sure not to include false positives

EXC_LASER_RESPONSE_PVAL = 0.5 #for selecting putative excitatory cells NOT responsive to laser
EXC_SPIKE_WIDTH = 0.0004

PV_CHR2_MICE = ['band004', 'band026', 'band032', 'band033']
SOM_CHR2_MICE = ['band005', 'band015', 'band016', 'band027', 'band028', 'band029', 'band030', 'band031', 'band034','band037','band038','band044','band045','band054','band059','band060']


PV_CELLS = bestCells.query('laserPVal<{} and laserUStat>0 and subject=={}'.format(LASER_RESPONSE_PVAL,PV_CHR2_MICE))
SOM_CELLS = bestCells.query('laserPVal<{} and laserUStat>0 and subject=={}'.format(LASER_RESPONSE_PVAL,SOM_CHR2_MICE))
EXC_CELLS = bestCells.query('(laserPVal>{} or laserUStat<0) and spikeWidth>{} and subject=={}'.format(EXC_LASER_RESPONSE_PVAL,EXC_SPIKE_WIDTH,SOM_CHR2_MICE))


primaryCells = EXC_CELLS[EXC_CELLS['recordingSiteName'].str.contains('Primary auditory area')]
nonPrimaryCells = EXC_CELLS[~EXC_CELLS['recordingSiteName'].str.contains('Primary auditory area')]

primarySIs = primaryCells['fitSustainedSuppressionIndexNoZeroHighAmp']
nonPrimarySIs = nonPrimaryCells['fitSustainedSuppressionIndexNoZeroHighAmp']

excCellSIs = np.array(EXC_CELLS['fitSustainedSuppressionIndexNoZeroHighAmp'])
excCellDepths = np.array(EXC_CELLS['cortexRatioDepth'])
notNanInds1 = np.where(~np.isnan(excCellDepths))[0]

plt.figure()
plt.subplot(1,3,1)
plt.hold(True)
plt.plot(excCellDepths,excCellSIs, 'ko', ms=5)
slope, intercept, rVal, pVal, stdErr = scipy.stats.linregress(excCellDepths[notNanInds1], excCellSIs[notNanInds1])
xvals = np.linspace(0,1,200)
yvals = slope*xvals + intercept
plt.plot(xvals, yvals, 'k-', zorder=-1)
print('SI vs depth: r={0}, p={1}'.format(rVal, pVal))

plt.xlim(-0.1,1.1)
plt.ylim(-0.1,1.1)
plt.ylabel('Suppression Index', fontsize=FONTSIZE)
plt.xlabel('Depth from pia (fraction of cortical thickness)', fontsize=FONTSIZE)

plt.subplot(1,3,3)
for ind, category in enumerate([primarySIs, nonPrimarySIs]):
    xval = (ind+1)*np.ones(len(category))
      
    jitterAmt = np.random.random(len(xval))
    xval = xval + (0.4 * jitterAmt) - 0.2
      
    plt.hold(True)
    plt.plot(xval, category, 'o', mfc='none', clip_on=False)
    median = np.median(category)
    #sem = stats.sem(vals[category])
    plt.plot([ind+0.7,ind+1.3], [median,median], '-', color='k', lw=3)

plt.xlim(0,3)
plt.ylim(-0.05,1.05)
plt.ylabel('Suppression Index', fontsize=FONTSIZE)
ax = plt.gca()
ax.set_xticks(range(1,3))
ax.set_xticklabels(['primary', 'not primary'], fontsize=FONTSIZE)#, rotation=-45)
plt.show()

pval = scipy.stats.ranksums(primarySIs, nonPrimarySIs)[1]
print('Primary vs non primary SIs p val: {}'.format(pval))

db2 = celldatabase.load_hdf('/mnt/jarahubdata/figuresdata/2018acsup/inactivation_cells_full.h5')
#db2 = celldatabase.load_hdf('/tmp/inactivation_cells.h5')
bestCells2 = db2.query('isiViolations<0.02')
bestCells2 = bestCells2.query('spikeShapeQuality>2.5 and tuningFitR2>0.1 and octavesFromPrefFreq<0.3 and sustainedSoundResponsePVal<0.05')

PV_ARCHT_MICE = ['band056','band058','band062','band072','band097', 'band102']
SOM_ARCHT_MICE = ['band055', 'band057','band073']

PV_INACTIVATED_CELLS = bestCells2.query('baselineChangeFR>0 and controlSession==0 and subject=={}'.format(PV_ARCHT_MICE))
SOM_INACTIVATED_CELLS = bestCells2.query('baselineChangeFR>0 and controlSession==0 and subject=={}'.format(SOM_ARCHT_MICE))

PVdepths = np.array(PV_INACTIVATED_CELLS['cortexRatioDepth'])
SOMdepths = np.array(SOM_INACTIVATED_CELLS['cortexRatioDepth'])

PVSI = PV_INACTIVATED_CELLS['fitSustainedSuppressionIndexNoZeroNoLaser']
SOMSI = SOM_INACTIVATED_CELLS['fitSustainedSuppressionIndexNoZeroNoLaser']

PVSILaser = PV_INACTIVATED_CELLS['fitSustainedSuppressionIndexNoZeroLaser']
SOMSILaser = SOM_INACTIVATED_CELLS['fitSustainedSuppressionIndexNoZeroLaser']

SOMSIdiff = np.array(SOMSILaser-SOMSI)
PVSIdiff = np.array(PVSILaser-PVSI)

plt.subplot(1,3,2)
l1, = plt.plot(SOMdepths, SOMSIdiff, 'ro', ms=5, mec='none')
l2, = plt.plot(PVdepths, PVSIdiff, 'bo', ms=5, mec='none')
plt.legend([l1,l2], ['no SOM', 'no PV'], loc='best', numpoints=1, handlelength=0.3, markerscale=1.7, frameon=False,)

notNanInds = np.where(~np.isnan(SOMdepths))[0]
slope, intercept, rVal, pVal, stdErr = scipy.stats.linregress(SOMdepths[notNanInds], SOMSIdiff[notNanInds])
xvals = np.linspace(0,1,200)
yvals = slope*xvals + intercept
#plt.plot(xvals, yvals, 'r-', zorder=-1)
print('no SOM SI vs depth: r={0}, p={1}'.format(rVal, pVal))

notNanInds = np.where(~np.isnan(PVdepths))[0]
slope, intercept, rVal, pVal, stdErr = scipy.stats.linregress(PVdepths[notNanInds], PVSIdiff[notNanInds])
xvals = np.linspace(0,1,200)
yvals = slope*xvals + intercept
#plt.plot(xvals, yvals, 'b-', zorder=-1)
print('no PV SI vs depth: r={0}, p={1}'.format(rVal, pVal))

plt.xlim(-0.1,1.1)
plt.ylim(-0.5,0.4)
plt.ylabel('Change in Suppression Index', fontsize=FONTSIZE)
plt.xlabel('Depth from pia (fraction of cortical thickness)', fontsize=FONTSIZE)
plt.show()