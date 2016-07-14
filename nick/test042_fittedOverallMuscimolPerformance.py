from jaratoolbox.test.nick import behavioranalysis_vnick as behavioranalysis
from jaratoolbox import extrastats
from matplotlib import pyplot as plt
import numpy as np

salChordEsts = np.zeros([2, 4])
musChordEsts = np.zeros([2, 4])
salModEsts = np.zeros([2, 4])
musModEsts = np.zeros([2, 4])


animals = ['amod002', 'amod003']
nAnimals = len(animals)

muscimolSessions = ['20160413a', '20160415a', '20160417a', '20160419a', '20160421a']
salineSessions = ['20160412a', '20160414a', '20160416a', '20160418a', '20160420a']

## -- Figure with all animals

plt.figure()

for indAnimal, animal in enumerate(animals):
    muscimolDataObjs, muscimolSoundTypes = behavioranalysis.load_behavior_sessions_sound_type(animal, muscimolSessions)
    salineDataObjs, salineSoundTypes = behavioranalysis.load_behavior_sessions_sound_type(animal, salineSessions)

    mdataChords = muscimolDataObjs[muscimolSoundTypes['chords']]
    sdataChords = salineDataObjs[salineSoundTypes['chords']]

    mdataMod = muscimolDataObjs[muscimolSoundTypes['amp_mod']]
    sdataMod = salineDataObjs[salineSoundTypes['amp_mod']]

    subplot2grid((nAnimals, 2), (indAnimal, 0))
    salChordEsts[indAnimal,:] = plot_psycurve_fit_and_data(sdataChords, 'k')
    musChordEsts[indAnimal,:] = plot_psycurve_fit_and_data(mdataChords, 'r')
    title('{},{}'.format(animal, 'chords'))

    subplot2grid((nAnimals, 2), (indAnimal, 1))
    salModEsts[indAnimal,:] = plot_psycurve_fit_and_data(sdataMod, 'k')
    musModEsts[indAnimal,:] = plot_psycurve_fit_and_data(mdataMod, 'r')
    title('{},{}'.format(animal, 'amp_mod'))

plt.figure



def plot_psycurve_fit_and_data(bdata, plotColor):
    #Calculate the psychometric
    rightTrials = bdata['choice']==bdata.labels['choice']['right']
    freqEachTrial = bdata['targetFrequency']
    valid = bdata['valid']
    (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue) = behavioranalysis.calculate_psychometric(rightTrials, freqEachTrial, valid)

    #Calculate the psycurve fit
    estimate = behavioranalysis.psycurve_fit_from_bdata(bdata, plotFits=0)

    #Plot in log2 space(fit is already in this space)
    possibleValues = np.log2(possibleValues)

    #Plot the stuff
    ax = plt.gca()
    plt.hold(1)
    xRange = possibleValues[-1]-possibleValues[1]
    fitxval = np.linspace(possibleValues[0]-0.1*xRange,possibleValues[-1]+0.1*xRange,40)
    fityvals = extrastats.psychfun(fitxval, *estimate)

    upperWhisker = ciHitsEachValue[1,:]-fractionHitsEachValue
    lowerWhisker = fractionHitsEachValue-ciHitsEachValue[0,:]
    (pline, pcaps, pbars) = plt.errorbar(possibleValues, fractionHitsEachValue,
                                            yerr = [lowerWhisker, upperWhisker],color='k', fmt=None)
    pdots = plt.plot(possibleValues, fractionHitsEachValue, 'o',mec='none',mfc='k',ms=8)

    setp(pcaps, color=plotColor)
    setp(pbars, color=plotColor)
    setp(pdots, markerfacecolor=plotColor)

    if np.unique(freqEachTrial)[0]<1000: #If Hz
        ax.set_xticks(possibleValues)
        ax.set_xticklabels(np.unique(freqEachTrial))
        plt.xlabel('Frequency (Hz)')
    else:
        ax.set_xticks(possibleValues)
        freqLabels = ['{:.03}'.format(x) for x in np.unique(freqEachTrial)/1000.0]
        ax.set_xticklabels(freqLabels)
        plt.xlabel('Frequency (kHz)')


    ax.plot(fitxval, fityvals, color=plotColor)
    plt.ylim([0, 1])
    plt.ylabel('Fraction Rightward Trials')

    return estimate

