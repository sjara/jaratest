from jaratoolbox.test.nick import behavioranalysis_vnick as behavioranalysis
from jaratoolbox import extraplots
from jaratoolbox import colorpalette

animal = 'amod004'
session = '20160502a'


dataObjs, soundTypes = behavioranalysis.load_behavior_sessions_sound_type(animal, [session])

figure()
clf()
bdata = dataObjs[soundTypes['tones']]
ax = subplot(121)
est = plot_psycurve_fit_and_data(bdata, 'k')
extraplots.boxoff(ax)
extraplots.set_ticks_fontsize(ax, 20)
fitline = ax.lines[3]
setp(fitline, lw=3)
setp(fitline, color=colorpalette.TangoPalette['Chameleon2'])
# pcaps= ax.lines[0]
# pbars = ax.lines[2]
# setp(pcaps, lw=2)
# setp(pbars, lw=2)
xticklabels = [item.get_text() for item in ax.get_xticklabels()]
xticks = ax.get_xticks()
newXtickLabels = logspace(xticks[0], xticks[-1], 3, base=2)
plt.ylim(-0.03, 1.03)

ax.set_xticks(np.log2(np.array(newXtickLabels)))
ax.set_xticklabels(['{:.3}'.format(x/1000.0) for x in newXtickLabels])
plt.show()



bdata = dataObjs[soundTypes['amp_mod']]
ax = subplot(122)
est = plot_psycurve_fit_and_data(bdata, 'k')
extraplots.boxoff(ax)
extraplots.set_ticks_fontsize(ax, 20)
fitline = ax.lines[3]

setp(fitline, lw=3)
setp(fitline, color=colorpalette.TangoPalette['SkyBlue2'])

xticklabels = [item.get_text() for item in ax.get_xticklabels()]
xticks = ax.get_xticks()
newXtickLabels = logspace(xticks[0], xticks[-1], 3, base=2)

ax.set_xticks(np.log2(np.array(newXtickLabels)))
ax.set_xticklabels(['{:.3}'.format(x) for x in newXtickLabels])

plt.ylim(-0.03, 1.03)


fig = plt.gcf()
fig.subplots_adjust(bottom=0.2)

plt.show()

savefig('/home/nick/Dropbox/terms/y2spring/dac/psycurves.svg')

fitcolor = colorpalette.TangoPalette['SkyBlue2']

def nice_psycurve_settings(ax, fitcolor=None, fontsize=20):

    '''
    A hack for setting some psycurve axes properties, especially the weight of the line and the xticks
    I made this because I am using the fxn plot_psycurve_fit_and_data, which obscures handles to things
    that I later need (like the lines, etc. ) This function will be useless if I make plots in a better way. 

    '''

    extraplots.boxoff(ax)
    extraplots.set_ticks_fontsize(ax, fontsize)
    fitline = ax.lines[3]
    plt.setp(fitline, lw=3)

    if fitcolor:
        plt.setp(fitline, color=fitcolor)

    xticklabels = [item.get_text() for item in ax.get_xticklabels()]
    xticks = ax.get_xticks()
    newXtickLabels = logspace(xticks[0], xticks[-1], 3, base=2)

    ax.set_xticks(np.log2(np.array(newXtickLabels)))
    if min(newXtickLabels) > 1000:
        ax.set_xticklabels(['{:.3}'.format(x/1000.0) for x in newXtickLabels])
    else:
        ax.set_xticklabels(['{:.3}'.format(x) for x in newXtickLabels])
