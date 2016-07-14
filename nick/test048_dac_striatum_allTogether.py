from jaratoolbox.test.nick import behavioranalysis_vnick as behavioranalysis
animals = ['adap023', 'adap022', 'adap026', 'adap027', 'adap030']
nAnimals = len(animals)

# muscimolSessions = ['20160601a', '20160603a', '20160607a']
# salineSessions = ['20160531a', '20160602a', '20160606a']

salineSessions = {'adap023': ['20160428a', '20160430a', '20160502a', '20160504b', '20160506a', '20160508a'],
                  'adap022': ['20160531a', '20160602a', '20160606a', '20160608a', '20160610a'],
                  'adap026': ['20160531a', '20160602a', '20160606a', '20160608a', '20160610a'],
                  'adap027': ['20160531a', '20160602a', '20160606a', '20160608a', '20160610a'],
                  'adap030': ['20160531a', '20160602a', '20160606a', '20160608a', '20160610a']
}

muscimolSessions = {'adap023': ['20160429a', '20160501a', '20160503a', '20160505a', '20160507a', '20160509a'],
                   'adap022': ['20160601a', '20160603a', '20160607a', '20160609a', '20160611a'],
                   'adap026': ['20160601a', '20160603a', '20160607a', '20160609a', '20160611a'],
                   'adap027': ['20160601a', '20160603a', '20160607a', '20160609a', '20160611a'],
                   'adap030': ['20160601a', '20160603a', '20160607a', '20160609a', '20160611a']
}

salChordEsts = np.zeros([nAnimals, 4])
musChordEsts = np.zeros([nAnimals, 4])


for indAnimal, animal in enumerate(animals):

    # ax = subplot2grid((1, nAnimals), (0, indAnimal))
    ax = subplot(2, 3, indAnimal)

    mdata = behavioranalysis.load_many_sessions(animal, muscimolSessions[animal])
    sdata = behavioranalysis.load_many_sessions(animal, salineSessions[animal])

    musChordEsts[indAnimal,:] = behavioranalysis.plot_psycurve_fit_and_data(mdata, 'r')
    salChordEsts[indAnimal,:] = behavioranalysis.plot_psycurve_fit_and_data(sdata, 'k')


    plt.ylim(-0.03, 1.03)
    behavioranalysis.nice_psycurve_settings(ax, fontsize=9, lineweight=2, fitlineinds=[3, 7])

    title(animal)

mc = musChordEsts[:,1]
sc = salChordEsts[:,1]

figure()
plot(zeros((len(sc), 1)), 1/(4.*sc), 'ko')
plot(ones((len(mc), 1)), 1/(4.*mc), 'ro')
xlim([-1, 2])
gca().set_xticks([0, 1])
gca().set_xticklabels(['saline', 'muscimol'])
ylabel('fraction going to right / octave (1/4b)')
title('chords')
