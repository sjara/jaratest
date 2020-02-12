import os
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
import matplotlib.colors

from jaratoolbox import celldatabase
from jaratoolbox import extraplots
from jaratoolbox import settings

FONTSIZE = 14

dbFilename = os.path.join(settings.FIGURES_DATA_PATH, '2018acsup', 'photoidentification_cells.h5')
#db = celldatabase.load_hdf(dbFilename)
db = celldatabase.load_hdf('/tmp/photoidentification_cells_0.h5')
bestCells = db.query('isiViolations<0.02 or modifiedISI<0.02')
#bestCells = bestCells.query('spikeShapeQuality>2.5 and tuningFitR2>0.1 and octavesFromPrefFreq<0.3 and sustainedSoundResponsePVal<0.05')
bestCells = bestCells.query('spikeShapeQuality>2.5 and tuningFitR2>0.1 and octavesFromPrefFreq<0.3 and onsetSoundResponsePVal<0.05')

LASER_RESPONSE_PVAL = 0.001 #want to be EXTRA sure not to include false positives

EXC_LASER_RESPONSE_PVAL = 0.5 #for selecting putative excitatory cells NOT responsive to laser
EXC_SPIKE_WIDTH = 0.0004

PV_CHR2_MICE = ['band004', 'band026', 'band032', 'band033']
SOM_CHR2_MICE = ['band005', 'band015', 'band016', 'band027', 'band028', 'band029', 'band030', 'band031', 'band034','band037','band038','band044','band045','band054','band059','band060']


PV_CELLS = bestCells.query('laserPVal<{} and laserUStat>0 and subject=={}'.format(LASER_RESPONSE_PVAL,PV_CHR2_MICE))
SOM_CELLS = bestCells.query('laserPVal<{} and laserUStat>0 and subject=={}'.format(LASER_RESPONSE_PVAL,SOM_CHR2_MICE))
EXC_CELLS = bestCells.query('(laserPVal>{} or laserUStat<0) and spikeWidth>{} and subject=={}'.format(EXC_LASER_RESPONSE_PVAL,EXC_SPIKE_WIDTH,SOM_CHR2_MICE))

PVonsetSIs = np.array(PV_CELLS['fitOnsetSuppressionIndexNoZero'])
SOMonsetSIs = np.array(SOM_CELLS['fitOnsetSuppressionIndexNoZero'])
excOnsetSIs = np.array(EXC_CELLS['fitOnsetSuppressionIndexNoZero'])

cellTypeColours = ['k', 'b', 'r']
    
categoryLabels = ['Exc.', r'PV$^+$', r'SOM$^+$']
    
axScatter = plt.subplot(1,2,1)
plt.hold(1)

suppressionVals = [excOnsetSIs, PVonsetSIs, SOMonsetSIs]
    
for category in range(len(suppressionVals)):
    edgeColour = matplotlib.colors.colorConverter.to_rgba(cellTypeColours[category], alpha=0.5)
    xval = (category+1)*np.ones(len(suppressionVals[category]))
      
    jitterAmt = np.random.random(len(xval))
    xval = xval + (0.4 * jitterAmt) - 0.2
      
    plt.hold(True)
    plt.plot(xval, suppressionVals[category], 'o', mec=edgeColour, mfc='none')
    median = np.median(suppressionVals[category])
    #sem = stats.sem(vals[category])
    plt.plot([category+0.7,category+1.3], [median,median], '-', color='k', mec=cellTypeColours[category], lw=3)  

plt.xlim(0,len(suppressionVals)+1)
plt.ylim(-0.05,1.05)
plt.ylabel('Onset Suppression Index', fontsize=FONTSIZE)
axScatter.set_xticks(range(1,len(suppressionVals)+1))
axScatter.set_xticklabels(categoryLabels, fontsize=FONTSIZE)#, rotation=-45)
extraplots.boxoff(axScatter)
yLims = np.array(plt.ylim())
extraplots.significance_stars([1,2], yLims[1]*1.03, yLims[1]*0.02, gapFactor=0.25)
plt.hold(0)

ExcPV = scipy.stats.ranksums(excOnsetSIs, PVonsetSIs)[1]
ExcSOM = scipy.stats.ranksums(excOnsetSIs, SOMonsetSIs)[1]
PVSOM = scipy.stats.ranksums(PVonsetSIs, SOMonsetSIs)[1]
print "Difference in suppression p vals: \nExc-PV: {0}\nExc-SOM: {1}\nPV-SOM: {2}".format(ExcPV,ExcSOM,PVSOM)

dbFilename2 = os.path.join(settings.FIGURES_DATA_PATH, '2018acsup', 'inactivation_cells_full.h5')
# db2 = celldatabase.load_hdf(dbFilename)
db2 = celldatabase.load_hdf('/tmp/inactivation_cells_full.h5')
bestCells2 = db2.query('isiViolations<0.02')
bestCells2 = bestCells2.query('spikeShapeQuality>2.5 and tuningFitR2>0.1 and octavesFromPrefFreq<0.3 and sustainedSoundResponsePVal<0.05')

PV_ARCHT_MICE = ['band056','band058','band062','band072','band097', 'band102']
SOM_ARCHT_MICE = ['band055', 'band057','band073']

PV_INACTIVATED_CELLS = bestCells2.query('baselineChangeFR>0 and controlSession==0 and subject=={}'.format(PV_ARCHT_MICE))
SOM_INACTIVATED_CELLS = bestCells2.query('baselineChangeFR>0 and controlSession==0 and subject=={}'.format(SOM_ARCHT_MICE))

PVSIs = np.array(PV_INACTIVATED_CELLS['onsetSuppressionIndexNoLaser'])
PVSIsLaser = np.array(PV_INACTIVATED_CELLS['onsetSuppressionIndexLaser'])

SOMSIs = np.array(SOM_INACTIVATED_CELLS['onsetSuppressionIndexNoLaser'])
SOMSIsLaser = np.array(SOM_INACTIVATED_CELLS['onsetSuppressionIndexLaser'])

axScatter2 = plt.subplot(1,2,2)
plt.hold(1)
l1, = plt.plot(PVSIs, PVSIsLaser, 'bo', ms=5, mec='none')
l2, = plt.plot(SOMSIs, SOMSIsLaser, 'ro', ms=5, mec='none')
plt.plot([-5,5],[-5,5], 'k--')
plt.legend([l1,l2], ['no PV', 'no SOM'], loc='best', numpoints=1, handlelength=0.3, markerscale=1.7, frameon=False)

plt.xlim(-0.05, 1.05)
plt.ylim(-0.05, 1.05)
plt.xlabel('Onset Suppression Index (Control)', fontsize=FONTSIZE)
plt.ylabel('Onset Suppression Index (Laser)', fontsize=FONTSIZE)
extraplots.boxoff(axScatter2)

noSOM = scipy.stats.wilcoxon(SOMSIs, SOMSIsLaser)[1]
noPV = scipy.stats.wilcoxon(PVSIs, PVSIsLaser)[1]
print "Change in suppression p vals: \nno SOM: {0}\nno PV: {1}".format(noSOM, noPV)

plt.show()