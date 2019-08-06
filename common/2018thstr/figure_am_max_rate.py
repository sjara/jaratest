
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from jaratoolbox import settings
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis
from jaratoolbox import celldatabase
from scipy import stats
import pandas as pd
import figparams
reload(figparams)


# dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_calculated_columns.h5')
dbPath = '/tmp/db_with_am_maxRate.h5'
db = celldatabase.load_hdf(dbPath)

goodISI = db.query('isiViolations<0.02 or modifiedISI<0.02')
goodShape = goodISI.query('spikeShapeQuality > 2')
goodLaser = goodShape.query("autoTagged==1 and subject != 'pinp018'")
# goodLaser = goodShape.query("autoTagged==1 and subject != 'pinp018' and summaryPulseLatency < 0.01")
goodNSpikes = goodLaser.query('nSpikes>2000')
goodPulseLatency = goodNSpikes.query('summaryPulseLatency<0.006')

dbToUse = goodNSpikes

dbToUse['evokedRateAM'] = dbToUse['maxRateAM'] - dbToUse['baseRateAM']

ac = dbToUse.groupby('brainArea').get_group('rightAC')
thal = dbToUse.groupby('brainArea').get_group('rightThal')

def jitter(arr, frac):
    jitter = (np.random.random(len(arr))-0.5)*2*frac
    jitteredArr = arr + jitter
    return jitteredArr

def medline(ax, yval, midline, width, color='k', linewidth=3):
    start = midline-(width/2)
    end = midline+(width/2)
    ax.plot([start, end], [yval, yval], color=color, lw=linewidth)

plt.clf()

messages = []

colorATh = figparams.cp.TangoPalette['SkyBlue2']
colorAC = figparams.cp.TangoPalette['ScarletRed1']
markerAlpha = 1


fullPanelWidthInches = 6.9 / 2
figSizeFactor = 1
figWidth = fullPanelWidthInches * (figSizeFactor)
# figHeight = figWidth / 2.5
figHeight = figWidth / 1
figSize = [figWidth, figHeight] # In inches

fontSizeModifier = 1.5
fontSizeLabels = figparams.fontSizeLabels * fontSizeModifier
fontSizeTicks = figparams.fontSizeTicks * fontSizeModifier #TODO: Why aren't we using the tick size var?
# fontSizeTicks = fontSizeLabels / 2.
fontSizePanel = figparams.fontSizePanel * fontSizeModifier
fontSizeTitles = figparams.fontSizeTitles * fontSizeModifier

#Params for extraplots significance stars
fontSizeNS = figparams.fontSizeNS * (fontSizeModifier*0.5)
fontSizeStars = figparams.fontSizeStars * (fontSizeModifier*0.5)
starHeightFactor = figparams.starHeightFactor
starGapFactor = figparams.starGapFactor
starYfactor = figparams.starYfactor

axMaxFR = plt.subplot(131)

popStatCol = 'maxRateAM'
acPopStat = ac[popStatCol][pd.notnull(ac[popStatCol])]
thalPopStat = thal[popStatCol][pd.notnull(thal[popStatCol])]

pos = jitter(np.ones(len(thalPopStat))*0, 0.20)
axMaxFR.plot(pos, thalPopStat, 'o', mec = colorATh, mfc = 'None', alpha=markerAlpha)
# axMaxFR.plot(pos, thalPopStat, 'o', mec = '0.5', mfc = 'None', alpha=markerAlpha)
medline(axMaxFR, np.median(thalPopStat), 0, 0.5)
# medline(axMaxFR, np.median(thalPopStat), 0, 0.8, color=colorATh)
pos = jitter(np.ones(len(acPopStat))*1, 0.20)
axMaxFR.plot(pos, acPopStat, 'o', mec = colorAC, mfc = 'None', alpha=markerAlpha)
# axMaxFR.plot(pos, acPopStat, 'o', mec = '0.5', mfc = 'None', alpha=markerAlpha)
medline(axMaxFR, np.median(acPopStat), 1, 0.5)
# medline(axMaxFR, np.median(acPopStat), 1, 0.8, color=colorAC)
axMaxFR.set_ylabel('Max FR (spk/s)', fontsize=fontSizeLabels)
# tickLabels = ['ATh:Str', 'AC:Str']
# tickLabels = ['ATh:Str\nn={}'.format(len(thalPopStat)), 'AC:Str\nn={}'.format(len(acPopStat))]
tickLabels = ['ATh:Str'.format(len(thalPopStat)), 'AC:Str'.format(len(acPopStat))]
axMaxFR.set_xticks(range(2))
axMaxFR.set_xlim([-0.5, 1.5])
extraplots.boxoff(axMaxFR)
extraplots.set_ticks_fontsize(axMaxFR, fontSizeTicks)
axMaxFR.set_xticklabels(tickLabels, fontsize=fontSizeLabels, rotation=45)


zstat, pVal = stats.mannwhitneyu(thalPopStat, acPopStat)

# print "Ranksums test between thalamus and AC population stat ({}) vals: p={}".format(popStatCol, pVal)
messages.append("{} p={}".format(popStatCol, pVal))

yDataMax = max([max(acPopStat), max(thalPopStat)])
yStars = yDataMax + yDataMax*starYfactor
yStarHeight = (yDataMax*starYfactor)*starHeightFactor
plt.sca(axMaxFR)

# starString = None if pVal<0.05 else 'n.s.'
if pVal<0.05:
    starString = None
    starSize = fontSizeStars
else:
    starString = 'n.s.'
    starSize = fontSizeNS

extraplots.significance_stars([0, 1], yStars, yStarHeight, starMarker='*',
                                starSize=starSize, starString=starString,
                                gapFactor=starGapFactor)
plt.hold(1)



## -- Baseline firing -- ##

popStatCol = 'baseRateAM'

acPopStat = ac[popStatCol][pd.notnull(ac[popStatCol])]
thalPopStat = thal[popStatCol][pd.notnull(thal[popStatCol])]

axBaseFR = plt.subplot(132)

pos = jitter(np.ones(len(thalPopStat))*0, 0.20)
axBaseFR.plot(pos, thalPopStat, 'o', mec = colorATh, mfc = 'None', alpha=markerAlpha)
# axBaseFR.plot(pos, thalPopStat, 'o', mec = '0.5', mfc = 'None', alpha=markerAlpha)
medline(axBaseFR, np.median(thalPopStat), 0, 0.5)
# medline(axBaseFR, np.median(thalPopStat), 0, 0.8, color=colorATh)
pos = jitter(np.ones(len(acPopStat))*1, 0.20)
axBaseFR.plot(pos, acPopStat, 'o', mec = colorAC, mfc = 'None', alpha=markerAlpha)
# axBaseFR.plot(pos, acPopStat, 'o', mec = '0.5', mfc = 'None', alpha=markerAlpha)
medline(axBaseFR, np.median(acPopStat), 1, 0.5)
# medline(axBaseFR, np.median(acPopStat), 1, 0.8, color=colorAC)
axBaseFR.set_ylabel('Baseline FR (spk/s)', fontsize=fontSizeLabels)
# tickLabels = ['ATh:Str', 'AC:Str']
# tickLabels = ['ATh:Str\nn={}'.format(len(thalPopStat)), 'AC:Str\nn={}'.format(len(acPopStat))]
tickLabels = ['ATh:Str'.format(len(thalPopStat)), 'AC:Str'.format(len(acPopStat))]
axBaseFR.set_xticks(range(2))
axBaseFR.set_xlim([-0.5, 1.5])
extraplots.boxoff(axBaseFR)
extraplots.set_ticks_fontsize(axBaseFR, fontSizeTicks)
axBaseFR.set_xticklabels(tickLabels, fontsize=fontSizeLabels, rotation=45)


zstat, pVal = stats.mannwhitneyu(thalPopStat, acPopStat)

# print "Ranksums test between thalamus and AC population stat ({}) vals: p={}".format(popStatCol, pVal)
messages.append("{} p={}".format(popStatCol, pVal))

yDataMax = max([max(acPopStat), max(thalPopStat)])
yStars = yDataMax + yDataMax*starYfactor
yStarHeight = (yDataMax*starYfactor)*starHeightFactor
plt.sca(axBaseFR)

# starString = None if pVal<0.05 else 'n.s.'
if pVal<0.05:
    starString = None
    starSize = fontSizeStars
else:
    starString = 'n.s.'
    starSize = fontSizeNS

extraplots.significance_stars([0, 1], yStars, yStarHeight, starMarker='*',
                                starSize=starSize, starString=starString,
                                gapFactor=starGapFactor)
plt.hold(1)




## -- Evoked firing -- ##

popStatCol = 'evokedRateAM'

acPopStat = ac[popStatCol][pd.notnull(ac[popStatCol])]
thalPopStat = thal[popStatCol][pd.notnull(thal[popStatCol])]

axEvokedFR = plt.subplot(133)

pos = jitter(np.ones(len(thalPopStat))*0, 0.20)
axEvokedFR.plot(pos, thalPopStat, 'o', mec = colorATh, mfc = 'None', alpha=markerAlpha)
# axEvokedFR.plot(pos, thalPopStat, 'o', mec = '0.5', mfc = 'None', alpha=markerAlpha)
medline(axEvokedFR, np.median(thalPopStat), 0, 0.5)
# medline(axEvokedFR, np.median(thalPopStat), 0, 0.8, color=colorATh)
pos = jitter(np.ones(len(acPopStat))*1, 0.20)
axEvokedFR.plot(pos, acPopStat, 'o', mec = colorAC, mfc = 'None', alpha=markerAlpha)
# axEvokedFR.plot(pos, acPopStat, 'o', mec = '0.5', mfc = 'None', alpha=markerAlpha)
medline(axEvokedFR, np.median(acPopStat), 1, 0.5)
# medline(axEvokedFR, np.median(acPopStat), 1, 0.8, color=colorAC)
axEvokedFR.set_ylabel('Evoked FR, max-baseline (spk/s)', fontsize=fontSizeLabels)
# tickLabels = ['ATh:Str', 'AC:Str']
# tickLabels = ['ATh:Str\nn={}'.format(len(thalPopStat)), 'AC:Str\nn={}'.format(len(acPopStat))]
tickLabels = ['ATh:Str'.format(len(thalPopStat)), 'AC:Str'.format(len(acPopStat))]
axEvokedFR.set_xticks(range(2))
axEvokedFR.set_xlim([-0.5, 1.5])
extraplots.boxoff(axEvokedFR)
extraplots.set_ticks_fontsize(axEvokedFR, fontSizeTicks)
axEvokedFR.set_xticklabels(tickLabels, fontsize=fontSizeLabels, rotation=45)

zstat, pVal = stats.mannwhitneyu(thalPopStat, acPopStat)

# print "Ranksums test between thalamus and AC population stat ({}) vals: p={}".format(popStatCol, pVal)
messages.append("{} p={}".format(popStatCol, pVal))

yDataMax = max([max(acPopStat), max(thalPopStat)])
yStars = yDataMax + yDataMax*starYfactor
yStarHeight = (yDataMax*starYfactor)*starHeightFactor
plt.sca(axEvokedFR)

# starString = None if pVal<0.05 else 'n.s.'
if pVal<0.05:
    starString = None
    starSize = fontSizeStars
else:
    starString = 'n.s.'
    starSize = fontSizeNS

extraplots.significance_stars([0, 1], yStars, yStarHeight, starMarker='*',
                                starSize=starSize, starString=starString,
                                gapFactor=starGapFactor)
plt.hold(1)


plt.subplots_adjust(wspace = 0.7)

plt.show()

print "\nSTATISTICS:\n"
for message in messages:
    print(message)
print "\n"
