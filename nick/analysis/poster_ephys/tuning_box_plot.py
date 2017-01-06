from matplotlib import pyplot as plt
from collections import Counter
from jaratest.nick.stats import am_funcs
reload(am_funcs)
import pandas
import numpy as np
from jaratoolbox import colorpalette
from jaratoolbox import extraplots
from scipy import stats
# import matplotlib
# matplotlib.rcParams['svg.fonttype'] = 'none'

thaldbfn = '/home/nick/src/jaratest/nick/analysis/poster_ephys/thalamusdb_q10.pickle'
cortdbfn = '/home/nick/src/jaratest/nick/analysis/poster_ephys/cortexdb_q10.pickle'
thaldb = pandas.read_pickle(thaldbfn)
cortdb = pandas.read_pickle(cortdbfn)

laserTrainThresh = 1.5
noiseBurstThresh = 2
isiThresh = 4

thalNonID = thaldb[(thaldb['isiViolations']<isiThresh) & (thaldb['noiseburstMaxZ']>noiseBurstThresh) & (thaldb['lasertrainMaxZ']<laserTrainThresh)]
cortNonID = cortdb[(cortdb['isiViolations']<isiThresh) & (cortdb['noiseburstMaxZ']>noiseBurstThresh) & (cortdb['lasertrainMaxZ']<laserTrainThresh)]

thalID = thaldb[(thaldb['isiViolations']<isiThresh) & (thaldb['noiseburstMaxZ']>noiseBurstThresh) & (thaldb['lasertrainMaxZ']>laserTrainThresh)]
cortID = cortdb[(cortdb['isiViolations']<isiThresh) & (cortdb['noiseburstMaxZ']>noiseBurstThresh) & (cortdb['lasertrainMaxZ']>laserTrainThresh)]

thalamQNonID = thalNonID['Q10']
cortamQNonID = cortNonID['Q10']

thalamQID = thalID['Q10']
cortamQID = cortID['Q10']

# Dependence of mean FR on AM rate

plt.clf()
stdev = 0.05
markersize = 8
linewidth = 2

import matplotlib

thalColor = colorpalette.TangoPalette['Orange2']
cortColor = colorpalette.TangoPalette['Plum2']

nonID = np.concatenate([1/thalamQNonID.dropna().as_matrix(), 1/cortamQNonID.dropna().as_matrix()])
nonIDLabs = np.concatenate([np.zeros(len(thalamQNonID.dropna())), np.ones(len(cortamQNonID.dropna()))])

ID = np.concatenate([1/thalamQID.dropna().as_matrix(), 1/cortamQID.dropna().as_matrix()])
IDLabs = np.concatenate([np.zeros(len(thalamQID.dropna())), np.ones(len(cortamQID.dropna()))])

#Print some stats
# numbers



allBW10 = np.concatenate([nonID, ID])
allLabs = np.concatenate([nonIDLabs, IDLabs])
identified = np.concatenate([np.zeros(len(nonID)), np.ones(len(ID))])
idCategoryLabels = ['Identified' if i else 'Non-Identified' for i in identified]
locationCategoryLabels = ['Cortex' if i else 'Thalamus' for i in allLabs]

frame = pandas.DataFrame.from_dict({'BW10':allBW10, 'Location':locationCategoryLabels, 'Identified':idCategoryLabels})

colors = {'Thalamus':thalColor, 'Cortex':cortColor}

import seaborn as sns
sns.set(style='ticks', font_scale=2, font='sans-serif')

ax=plt.gca()
sns.set_style({"xtick.direction": "in","ytick.direction": "in"})
ax = sns.boxplot(y='BW10', x='Identified', data=frame, hue='Location', ax=ax, palette=colors)
ax.set(xticklabels=['Non-tagged', 'Tagged\n(project to striatum)'])
plt.ylim([0, 2])
extraplots.boxoff(ax)
fig = plt.gcf()
fig.set_size_inches(4.3, 3.9)

# sns.set(style="ticks")

# # Load the example tips dataset
# tips = sns.load_dataset("tips")

# # Draw a nested boxplot to show bills by day and sex
# sns.boxplot(x="day", y="total_bill", hue="sex", data=tips, palette="PRGn")
# sns.despine(offset=10, trim=True)
# # 
linewidth=2
for i,artist in enumerate(ax.artists):
    # Set the linecolor on the artist to the facecolor, and set the facecolor to None
    col = artist.get_facecolor()
    artist.set_edgecolor(col)
    if i<2:
        artist.set_facecolor('None')
    else:
        artist.set_alpha(0.8)
    artist.set_linewidth(linewidth)

    # Each box has 6 associated Line2D objects (to make the whiskers, fliers, etc.)
    # Loop over them here, and use the same colour as above
    for j in range(i*6,i*6+6):
        line = ax.lines[j]
        line.set_color(col)
        line.set_mfc(col)
        line.set_mec(col)
        line.set_linewidth(linewidth)

# Also fix the legend
for legpatch in ax.get_legend().get_patches():
    col = legpatch.get_facecolor()
    legpatch.set_edgecolor(col)
    # legpatch.set_facecolor('None')

sns.plt.show()

fig = plt.gcf()
fig.set_size_inches(4, 2.95)
plt.xlabel('')
plt.tight_layout()
