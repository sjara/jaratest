from jaratoolbox.test.nick import behavioranalysis_vnick as behavioranalysis
from jaratoolbox import extrastats
from matplotlib import pyplot as plt
import numpy as np



# animals = ['amod003']
# animals = ['amod003']

# muscimolSessions = ['20160413a', '20160415a', '20160417a', '20160419a', '20160421a']
# salineSessions = ['20160412a', '20160414a', '20160416a', '20160418a', '20160420a']

# animals = ['amod004']
animals = ['amod002', 'amod003']
muscimolSessions = {'amod004':['20160427a', '20160429a', '20160501a', '20160503a', '20160505a', '20160507a', '20160509a'], 'amod002':['20160413a', '20160415a', '20160417a', '20160419a', '20160421a'], 'amod003':['20160413a', '20160415a', '20160417a', '20160419a', '20160421a']}

salineSessions = {'amod004':['20160426a', '20160428a', '20160430a', '20160502a', '20160504a', '20160506a', '20160508a'], 'amod002':['20160412a', '20160414a', '20160416a', '20160418a', '20160420a'], 'amod003':['20160412a', '20160414a', '20160416a', '20160418a', '20160420a']}

nAnimals = len(animals)
plt.figure()

salChordEsts = np.zeros([nAnimals, 4])
musChordEsts = np.zeros([nAnimals, 4])
salModEsts = np.zeros([nAnimals, 4])
musModEsts = np.zeros([nAnimals, 4])

for indAnimal, animal in enumerate(animals):
    muscimolDataObjs, muscimolSoundTypes = behavioranalysis.load_behavior_sessions_sound_type(animal, muscimolSessions[animal])
    salineDataObjs, salineSoundTypes = behavioranalysis.load_behavior_sessions_sound_type(animal, salineSessions[animal])

    mdataChords = muscimolDataObjs[muscimolSoundTypes['chords']]
    sdataChords = salineDataObjs[salineSoundTypes['chords']]

    mdataMod = muscimolDataObjs[muscimolSoundTypes['amp_mod']]
    sdataMod = salineDataObjs[salineSoundTypes['amp_mod']]

    # mdataChords = muscimolDataObjs[muscimolSoundTypes['tones']]
    # sdataChords = salineDataObjs[salineSoundTypes['tones']]

    # mdataMod = muscimolDataObjs[muscimolSoundTypes['amp_mod']]
    # sdataMod = salineDataObjs[salineSoundTypes['amp_mod']]

    subplot2grid((2, nAnimals), (0, indAnimal))
    salChordEsts[indAnimal,:] = plot_psycurve_fit_and_data(sdataChords, 'k')
    musChordEsts[indAnimal,:] = plot_psycurve_fit_and_data(mdataChords, 'r')
    title('{},{}'.format(animal, 'chords'))

    ax = gca()
    extraplots.boxoff(ax)
    extraplots.set_ticks_fontsize(ax, 20)
    fitline = ax.lines[3]
    setp(fitline, lw=3)
    fitline2 = ax.lines[7]
    setp(fitline2, lw=3)
    xticklabels = [item.get_text() for item in ax.get_xticklabels()]
    xticks = ax.get_xticks()
    newXtickLabels = logspace(xticks[0], xticks[-1], 3, base=2)
    ax.set_xticks(np.log2(np.array(newXtickLabels)))
    ax.set_xticklabels(['{:.3}'.format(x/1000.0) for x in newXtickLabels])

    plt.ylim(-0.03, 1.03)


    subplot2grid((2, nAnimals), (1, indAnimal))
    salModEsts[indAnimal,:] = plot_psycurve_fit_and_data(sdataMod, 'k')
    musModEsts[indAnimal,:] = plot_psycurve_fit_and_data(mdataMod, 'r')
    title('{},{}'.format(animal, 'amp_mod'))

    ax = gca()
    extraplots.boxoff(ax)
    extraplots.set_ticks_fontsize(ax, 20)
    fitline = ax.lines[3]
    fitline2 = ax.lines[7]
    setp(fitline, lw=3)
    setp(fitline2, lw=3)
    xticklabels = [item.get_text() for item in ax.get_xticklabels()]
    xticks = ax.get_xticks()
    newXtickLabels = logspace(xticks[0], xticks[-1], 3, base=2)
    ax.set_xticks(np.log2(np.array(newXtickLabels)))
    ax.set_xticks(np.log2(np.array(newXtickLabels)))

    ax.set_xticklabels(['{:.3}'.format(x) for x in newXtickLabels])
    plt.ylim(-0.03, 1.03)


fig = plt.gcf()
plt.tight_layout()

plt.show()



sa = salModEsts[:,1]
ma = musModEsts[:,1]
sc = salChordEsts[:,1]
mc = musChordEsts[:,1]

figure()
subplot(121)
plot(zeros((len(sa), 1)), 1/(4.*sa), 'ko')
plot(ones((len(ma), 1)), 1/(4.*ma), 'ro')
xlim([-1, 2])
gca().set_xticks([0, 1])
gca().set_xticklabels(['saline', 'muscimol'])
ylabel('fraction going to right / octave (1/4b)')
title('amp_mod')
show()

subplot(122)
cla()
plot(zeros((len(sc), 1)), 1/(4.*sc), 'ko')
plot(ones((len(mc), 1)), 1/(4.*mc), 'ro')
xlim([-1, 2])
gca().set_xticks([0, 1])
gca().set_xticklabels(['saline', 'muscimol'])
ylabel('fraction going to right / octave (1/4b)')
title('chords')
ylim([1.9, 2.55])


savefig('/home/nick/Dropbox/terms/y2spring/dac/ACMuscimolData.svg')
