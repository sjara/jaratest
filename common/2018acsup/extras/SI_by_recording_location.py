import numpy as np
import scipy.stats
import matplotlib.pyplot as plt

from jaratoolbox import celldatabase

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
plt.ylabel('Suppression Index')
ax = plt.gca()
ax.set_xticks(range(1,3))
ax.set_xticklabels(['primary', 'not primary'], rotation=-45)
plt.show()
