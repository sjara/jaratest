from jaratoolbox.test.nick import behavioranalysis_vnick as behavioranalysis
from jaratoolbox import extrastats
from matplotlib import pyplot as plt
import numpy as np



animal = 'adap027'
nAnimals = len(animals)

muscimolSessions = ['20160601a', '20160603a', '20160607a']
salineSessions = ['20160531a', '20160602a', '20160606a']

salChordEsts = np.zeros([len(salineSessions), 4])
musChordEsts = np.zeros([len(muscimolSessions), 4])

plt.figure()

for indSession, session in enumerate(salineSessions):
    ax = subplot2grid((2, len(muscimolSessions)), (0, indSession))

    sdata = behavioranalysis.load_many_sessions(animal, [session])
    salChordEsts[indSession,:] = plot_psycurve_fit_and_data(sdata, 'k')
    behavioranalysis.nice_psycurve_settings(ax, fontsize=9, lineweight=2)
    plt.ylim(-0.03, 1.03)

for indSession, session in enumerate(muscimolSessions):

    ax = subplot2grid((2, len(muscimolSessions)), (1, indSession))

    mdata = behavioranalysis.load_many_sessions(animal, [session])
    musChordEsts[indSession,:] = plot_psycurve_fit_and_data(mdata, 'r')
    # title('{},{}'.format(animal, 'chords'))

    plt.ylim(-0.03, 1.03)
    behavioranalysis.nice_psycurve_settings(ax, fontsize=9, lineweight=2)

suptitle(animal)


sc = salChordEsts[:,1]
mc = musChordEsts[:,1]


figure()
plot(zeros((len(sc), 1)), 1/(4.*sc), 'ko')
plot(ones((len(mc), 1)), 1/(4.*mc), 'ro')
xlim([-1, 2])
gca().set_xticks([0, 1])
gca().set_xticklabels(['saline', 'muscimol'])
ylabel('fraction going to right / octave (1/4b)')
title('chords')

show()


fig = plt.gcf()
plt.tight_layout()

plt.show()


savefig('/home/nick/Dropbox/terms/y2spring/dac/StriatumMuscimolData.svg')

