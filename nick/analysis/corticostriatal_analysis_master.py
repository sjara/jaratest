import pandas
from matplotlib import pyplot as plt
from collections import Counter
from jaratest.nick.stats import am_funcs
reload(am_funcs)
import numpy as np
from jaratoolbox import colorpalette
from jaratoolbox import extraplots
from scipy import stats
dbFolderFormat = '/home/nick/data/database/{}/{}_database.h5' #(mouse, mouse)

mice = ['pinp016', 'pinp017', 'pinp018']

dbs = []
for mouse in mice:
    dbFn = dbFolderFormat.format(mouse, mouse)
    db = pandas.read_hdf(dbFn, 'database')
    dbs.append(db)

masterdb = pandas.concat(dbs, ignore_index=True)

soundResponsive = masterdb.query('isiViolations<0.02 and shapeQuality>2 and noisePval<0.05')
soundLaserResponsive = soundResponsive.query('pulsePval<0.05 and trainRatio>0.8')

# soundResponsive['Identified'] = (soundResponsive.pulsePval<0.05) & (soundResponsive.trainRatio>0.8)


# # thalSR = soundResponsive.query("brainarea == 'rightThal'")
# # cortSR = soundResponsive.query("brainarea == 'rightAC'")

# # thalSL = soundLaserResponsive.query("brainarea == 'rightThal'")
# # cortSL = soundLaserResponsive.query("brainarea == 'rightAC'")

# # thalamQNonID = thalSR['Q10']
# # cortamQNonID = cortSR['Q10']

# # thalamQID = thalSL['Q10']
# # cortamQID = cortSL['Q10']

# plt.clf()
# stdev = 0.05
# markersize = 8
# linewidth = 2

# import matplotlib

# thalColor = colorpalette.TangoPalette['Orange2']
# cortColor = colorpalette.TangoPalette['Plum2']

# colors = {'rightThal':thalColor, 'rightAC':cortColor}

# import seaborn as sns
# sns.set(style='ticks', font_scale=2, font='sans-serif')

# ax=plt.gca()
# sns.set_style({"xtick.direction": "in","ytick.direction": "in"})
# ax = sns.boxplot(y='Q10', x='Identified', data=soundResponsive, hue='brainarea', ax=ax, palette=colors)
# # ax.set(xticklabels=['Non-tagged', 'Tagged\n(project to striatum)'])
# plt.ylim([0, 2])
# extraplots.boxoff(ax)
# fig = plt.gcf()
# fig.set_size_inches(4.3, 3.9)

# # sns.set(style="ticks")

# # # Load the example tips dataset
# # tips = sns.load_dataset("tips")

# # # Draw a nested boxplot to show bills by day and sex
# # sns.boxplot(x="day", y="total_bill", hue="sex", data=tips, palette="PRGn")
# # sns.despine(offset=10, trim=True)
# # # 
# # linewidth=2
# # for i,artist in enumerate(ax.artists):
# #     # Set the linecolor on the artist to the facecolor, and set the facecolor to None
# #     col = artist.get_facecolor()
# #     artist.set_edgecolor(col)
# #     if i<2:
# #         artist.set_facecolor('None')
# #     else:
# #         artist.set_alpha(0.8)
# #     artist.set_linewidth(linewidth)

# #     # Each box has 6 associated Line2D objects (to make the whiskers, fliers, etc.)
# #     # Loop over them here, and use the same colour as above
# #     for j in range(i*6,i*6+6):
# #         line = ax.lines[j]
# #         line.set_color(col)
# #         line.set_mfc(col)
# #         line.set_mec(col)
# #         line.set_linewidth(linewidth)

# # # Also fix the legend
# # for legpatch in ax.get_legend().get_patches():
# #     col = legpatch.get_facecolor()
# #     legpatch.set_edgecolor(col)
# #     # legpatch.set_facecolor('None')

# sns.plt.show()

# fig = plt.gcf()
# fig.set_size_inches(4, 2.95)
# plt.xlabel('')
# plt.tight_layout()
