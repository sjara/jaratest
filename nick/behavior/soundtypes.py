import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import extraplots
from jaratoolbox import extrastats
from jaratoolbox import behavioranalysis
from jaratoolbox import colorpalette

FREQCOLORS = [colorpalette.TangoPalette['Chameleon3'],
              colorpalette.TangoPalette['ScarletRed1'],
              colorpalette.TangoPalette['SkyBlue2'],
              colorpalette.TangoPalette['Orange2']]

def load_behavior_sessions_sound_type(animal, sessions):

    '''
    Load many sessions (or only one) and then divide up into several bdata objects based on the type of
    sound that was presented.

    Args
    animal (str): The name of the animal
    sessions (list of strings): Sessions to load

    Returns
    dataObjs (list of jaratoolbox.behavioranalysis.LoadBehaviorData objects):
             Behavior data objects for each sound type
    dataSoundTypes (list of strings): The sound type that corresponds to each of the data objects

    '''

    bdata = behavioranalysis.load_many_sessions(animal, sessions)
    soundTypes = [bdata.labels['soundType'][x] for x in np.unique(bdata['soundType'])]

    dataObjs = []
    dataSoundTypes = {}

    for indType, thisType in enumerate(soundTypes):
        bdataThisType = behavioranalysis.load_many_sessions(animal, sessions)

        #The inds where this kind of sound was presented
        boolThisType = bdataThisType['soundType']==bdataThisType.labels['soundType'][thisType]

        #All other inds
        notBoolThisType = np.logical_not(boolThisType)

        notIndsThisType = np.flatnonzero(notBoolThisType)

        #Remove all trials where this type was not presented
        bdataThisType.remove_trials(notIndsThisType)

        #Save out the bdata object and the sound type
        dataObjs.append(bdataThisType)
        dataSoundTypes.update({thisType:indType})

    return (dataObjs, dataSoundTypes)

def plot_multiple_psycurves(bdataList, colorsList, fontsize=12):

    '''
    Nick 2016-05-20

    Plots psychometric curves for bdata objects in different colors on the same plot

    Args:

    bdataList (list of jaratoolbox.loadbehavior.LoadBehaviorData objects): list of bdata to plot
    colorsList (list of str): list of color strings the same length as bdataList ('k', 'b', etc.)
    fontsize (int): Size of the label font for the figure
    '''

    plt.hold(1)
    for ind, bdata in enumerate(bdataList):
        rightTrials = bdata['choice']==bdata.labels['choice']['right']
        freqEachTrial = bdata['targetFrequency']
        valid = bdata['valid']

        (possibleValues,
         fractionHitsEachValue,
         ciHitsEachValue,
         nTrialsEachValue,
         nHitsEachValue)= calculate_psychometric(rightTrials,
                                                 freqEachTrial,
                                                 valid)

        (pline,
         pcaps,
         pbars,
         pdots) = extraplots.plot_psychometric(1e-3*possibleValues,
                                               fractionHitsEachValue,
                                               ciHitsEachValue,
                                               xTickPeriod=1)

        plt.xlabel('Frequency (kHz)',fontsize=fontsize)
        plt.ylabel('Rightward trials (%)',fontsize=fontsize)
        extraplots.set_ticks_fontsize(plt.gca(),fontsize)

        plt.setp(pline, color=colorsList[ind])
        plt.setp(pcaps, color=colorsList[ind])
        plt.setp(pbars, color=colorsList[ind])
        plt.setp(pdots, markerfacecolor=colorsList[ind])


def psycurve_fit_from_bdata(bdata, plotFits=True):

    '''
    Nick 2016-05-20

    Calculates psychometric curve fits in log2(freq) space.

    Args:

    bdata (jaratoolbox.loadbehavior.BehaviorData object): The bdata object to fit
    plotFits (bool): whether or not to plot the data and fitted curve to the current axis

    Returns:

    estimate (list of float): The parameter estimates for the psychometric function (alpha, beta, gamma, lambda - see jaratoolbox.extrastats.psychometric_fit)
    '''

    rightTrials = bdata['choice']==bdata.labels['choice']['right']
    freqEachTrial = bdata['targetFrequency']
    valid = bdata['valid']

    (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue) = calculate_psychometric(rightTrials, freqEachTrial, valid)

    possibleFreq = np.log2(np.unique(freqEachTrial))
    print 'FIXME: Arbitrary constraints for alpha pos!!'
    lowerFreqConstraint = possibleFreq[1]
    upperFreqConstraint = possibleFreq[-2]
    # lowerFreqConstraint = possibleFreq[0]
    # upperFreqConstraint = possibleFreq[-1]
    maxFreq = max(possibleFreq)
    minFreq = min(possibleFreq)


    constraints = ( 'Uniform({}, {})'.format(lowerFreqConstraint, upperFreqConstraint), 'Uniform(0,5)' ,'Uniform(0,0.5)', 'Uniform(0,0.5)')
    # constraints = ( 'unconstrained', 'Uniform(0,2)' ,'Uniform(0,1)', 'Uniform(0,1)')
    estimate = extrastats.psychometric_fit(possibleFreq, nTrialsEachValue, nHitsEachValue, constraints)

    if plotFits:
        ax = plt.gca()
        xRange = possibleFreq[-1]-possibleFreq[1]
        fitxval = np.linspace(possibleFreq[0]-0.1*xRange,possibleFreq[-1]+0.1*xRange,40)

        fityvals = extrastats.psychfun(fitxval, *estimate)

        ax.plot(possibleFreq, fractionHitsEachValue, 'bo')
        plt.hold(1)

        ax.plot(fitxval, fityvals)
        plt.ylim([0, 1])

    return estimate

def plot_psycurve_fit_and_data(bdata, plotColor):
    #Calculate the psychometric
    rightTrials = bdata['choice']==bdata.labels['choice']['right']
    freqEachTrial = bdata['targetFrequency']
    valid = bdata['valid']
    (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue) = calculate_psychometric(rightTrials, freqEachTrial, valid)

    #Calculate the psycurve fit
    estimate = psycurve_fit_from_bdata(bdata, plotFits=0)

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
                                            yerr = [lowerWhisker, upperWhisker],color='k', fmt=None, clip_on=False)
    pdots = plt.plot(possibleValues, fractionHitsEachValue, 'o',mec='none',mfc='k',ms=8, clip_on=False)

    plt.setp(pcaps, color=plotColor)
    plt.setp(pbars, color=plotColor)
    plt.setp(pdots, markerfacecolor=plotColor)

    if np.unique(freqEachTrial)[0]<1000: #If Hz
        ax.set_xticks(possibleValues)
        ax.set_xticklabels(np.unique(freqEachTrial))
        plt.xlabel('Frequency (Hz)')
    else:
        ax.set_xticks(possibleValues)
        freqLabels = ['{:.03}'.format(x) for x in np.unique(freqEachTrial)/1000.0]
        ax.set_xticklabels(freqLabels)
        plt.xlabel('Frequency (kHz)')


    ax.plot(fitxval, fityvals, color=plotColor, clip_on=False)
    plt.ylim([0, 1])
    plt.ylabel('Fraction Rightward Trials')

    return estimate

def nice_psycurve_settings(ax, fitcolor=None, fontsize=20, lineweight=3, fitlineinds=[3]):

    '''
    A hack for setting some psycurve axes properties, especially the weight of the line and the xticks
    I made this because I am using the fxn plot_psycurve_fit_and_data, which obscures handles to things
    that I later need (like the lines, etc. ) This function will be useless if I make plots in a better way.

    '''

    extraplots.boxoff(ax)
    extraplots.set_ticks_fontsize(ax, fontsize)


    for lineind in fitlineinds:
        fitline = ax.lines[lineind]
        plt.setp(fitline, lw=lineweight)

    if fitcolor:
        plt.setp(fitline, color=fitcolor)

    xticklabels = [item.get_text() for item in ax.get_xticklabels()]
    xticks = ax.get_xticks()
    newXtickLabels = np.logspace(xticks[0], xticks[-1], 3, base=2)

    ax.set_xticks(np.log2(np.array(newXtickLabels)))
    if min(newXtickLabels) > 1000:
        ax.set_xticklabels(['{:.3}'.format(x/1000.0) for x in newXtickLabels])
    else:
        ax.set_xticklabels(['{:.3}'.format(x) for x in newXtickLabels])

def sound_type_behavior_summary(subjects, sessions, output_dir, trialslim=None):

    '''
    Nick 2016-05-20

    Plots a report for behavior data that has multiple sound types. Will plot a psycurve for each sound type,
    and then a dynamics plot with the different sound types as different colored lines

    Args:
    subjects (list of str): The animals to plot (example: ['amod002', 'amod003'])
    sessions (list of str): The sessions to plot for each animal (example: ['20160529a'])
    output_dir (str): FIXME currently unused, for saving the report
    trialslim (list): upper and lower trial number to plot dynamics

    '''

    if isinstance(subjects,str):
        subjects = [subjects]
    if isinstance(sessions,str):
        sessions = [sessions]
    nSessions = len(sessions)
    nAnimals = len(subjects)

    for indAnimal, animalName in enumerate(subjects):
        for indSession, session in enumerate(sessions):
            #The sound types separated into different bdata objects
            try:
                (bdataObjs, bdataSoundTypes) = load_behavior_sessions_sound_type(animalName,
                                                                                 [session])
            except KeyError: #Will happen if the bdata does not have 'soundType' key'
                print "ERROR: Data for {} - {} may not be in the correct format".format(animalName, session)
                break

            #All the bdata together for plotting the dynamics
            allBehavData = behavioranalysis.load_many_sessions(animalName, [session])
            nSoundTypes = len(bdataSoundTypes) #This should hopefully be the same for all the animals being plotted

            #Keeps track of the min and max for each sound type for plotting dynamics
            allFreqsToUse = []

            #The y inds for plotting
            yInd = indAnimal + indSession + indAnimal*(nSessions-1)

            for indSoundType, soundType in enumerate(bdataSoundTypes):
                plt.subplot2grid((nAnimals*nSessions, nSoundTypes+2), (yInd, indSoundType))
                thisBehavData = bdataObjs[indSoundType]

                #Find min and max freqs for plotting
                possibleFreq = np.unique(thisBehavData['targetFrequency'])
                freqsToUse = [min(possibleFreq), max(possibleFreq)]
                allFreqsToUse.extend(freqsToUse)

                #Plot psycurves or summaries
                if any(thisBehavData['psycurveMode']):
                    (pline, pcaps, pbars, pdots) = behavioranalysis.plot_frequency_psycurve(thisBehavData)
                    thisColor = FREQCOLORS[indSoundType*2]
                    plt.setp(pline, color=thisColor)
                    plt.setp(pcaps, color=thisColor)
                    plt.setp(pbars, color=thisColor)
                    plt.setp(pdots, markerfacecolor=thisColor)
                    plt.title(soundType)
                    if not indSoundType==0:
                        plt.ylabel('')
                else:
                    thisBehavData.find_trials_each_block()
                    behavioranalysis.plot_summary(thisBehavData,fontsize=8,soundfreq=freqsToUse)
                    plt.title(soundType)

            #Plot the dynamics for all the sound types
            plt.subplot2grid((nAnimals*nSessions, nSoundTypes+2), (yInd, nSoundTypes), colspan=2)
            behavioranalysis.plot_dynamics(allBehavData, soundfreq = allFreqsToUse)
            plt.ylabel('')
            if trialslim:
                plt.xlim(trialslim)
            plt.title('{}, {}'.format(animalName, session))
            plt.subplots_adjust(hspace = 0.7)
