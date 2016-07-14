from jaratoolbox import settings
from jaratoolbox.test.nick import behavioranalysis_vnick as behavioranalysis
from jaratoolbox import extraplots
reload(behavioranalysis)

#### Making plot of average performance across time

clf()

## Settings for amod002 and amod003
# animal = 'amod003'
# sessions = ['20160412a', '20160413a', '20160414a', '20160415a', '20160416a', '20160417a', '20160418a', '20160419a', '20160420a', '20160421a', '20160422a', '20160423a', '20160424a', '20160425a', '20160426a', '20160427a', '20160428a', '20160429a', '20160430a', '20160501a', '20160502a']
# muscimol = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1]

# ## - Amod001 settings - I actually cant use these yet because the data format is different
# animal = 'amod001'
# sessions = ['20160323a', '20160322a', '20160321a', '20160320a', '20160319a', '20160318a', '20160317a', '20160316a', '20160315a', '20160314a']
# muscimol = [1, 0, 0, 1, 0, 1, 0, 1, 0, 1]

## - amod004 settings
clf()
animal = 'amod004'
sessions = ['20160426a','20160427a','20160428a','20160429a','20160430a','20160501a','20160502a','20160503a','20160504a','20160505a','20160506a','20160507a','20160508a','20160509a']
muscimol = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]



modPerf = []
chordPerf = []
modRewarded = []
modValid = []
chordRewarded = []
chordValid = []

for session in sessions:
    bdata = behavioranalysis.load_many_sessions(animal, [session])
    modP, nRewMod, nValMod = behavioranalysis.percent_correct_sound_type(bdata, 'amp_mod')
    chordP, nRewChords, nValChords = behavioranalysis.percent_correct_sound_type(bdata, 'tones')
    modPerf.append(modP)
    chordPerf.append(chordP)
    modRewarded.append(nRewMod)
    modValid.append(nValMod)
    chordRewarded.append(nRewChords)
    chordValid.append(nValChords)

from statsmodels.stats.proportion import proportion_confint

modCis = np.array(proportion_confint(array(modRewarded), array(modValid), method = 'wilson'))
chordCis = np.array(proportion_confint(array(chordRewarded), array(chordValid), method = 'wilson'))

# plot(modPerfs, 'g-o')
# hold(1)
# plot(chordPerfs, 'b-o')
# axhline(y=50, color='0.7')

xvals = range(len(muscimol))

upperModWhisker = modCis[1,:]-modPerf
lowerModWhisker = modPerf-modCis[0,:]
modError = np.vstack((upperModWhisker, lowerModWhisker))

(plineMod, pcapsMod, pbarsMod) = plt.errorbar(xvals, 100*array(modPerf),
                                        yerr = 100*modError,color='g')
pdotsMod = plt.plot(xvals, 100*array(modPerf), 'o',mec='none',mfc='g',ms=8, label='amp_mod')

upperChordWhisker = chordCis[1,:]-chordPerf
lowerChordWhisker = chordPerf-chordCis[0,:]
(plineChord, pcapsChord, pbarsChord) = plt.errorbar(xvals, 100*array(chordPerf),
                                        yerr = [100*lowerChordWhisker, 100*upperChordWhisker],color='b')
pdotsChord = plt.plot(xvals, 100*array(chordPerf), 'o',mec='none',mfc='b',ms=8, label='tones')

legend()

mLabels = ['M' if x==1 else 'S' for x in muscimol ]

ax = gca()
ax.set_xticks(range(len(mLabels)))

# ax.set_xticklabels(mLabels)
ax.set_xticklabels(sessions, rotation=40, ha='right')

colors = {0:'k', 1:'r'}

[label.set_color(colors[mus]) for label,mus in zip(plt.gca().get_xticklabels(), muscimol)]

xlim([-0.5, len(muscimol)-0.5])
ylim([40, 110])

yticks([50, 60, 70, 80, 90, 100])

axhline(50, color = '0.7')
axhline(100, color = '0.7')
margins(0.2)
plt.subplots_adjust(bottom=0.2)
title(animal)
ylabel('Average Percent Correct')
show()
