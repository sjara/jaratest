'''
Tools for analyzing behavioral data.
'''

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import extrafuncs
from jaratoolbox import extraplots
from jaratoolbox import extrastats
from jaratoolbox import loadbehavior
from jaratoolbox import settings
reload(settings)
from jaratoolbox import colorpalette

EXPERIMENTER = settings.DEFAULT_EXPERIMENTER
FREQCOLORS = [colorpalette.TangoPalette['Chameleon3'],
              colorpalette.TangoPalette['ScarletRed1'],
              colorpalette.TangoPalette['SkyBlue2'],
              colorpalette.TangoPalette['Orange2']]
#colorpalette.TangoPalette['Orange2']

def find_trials_each_type(parameter,parameterPossibleValues):
    '''
    Note that if you want to include only a subset of elements of the parameters array
    you can mask the output with something like:
    trialsEachType & mask[:,np.newaxis]
    '''
    nTrials = len(parameter)
    nValues = len(parameterPossibleValues)
    trialsEachType = np.zeros((nTrials,nValues),dtype=bool)
    for indval,paramValue in enumerate(parameterPossibleValues):
        trialsEachType[:,indval] = (parameter==paramValue)
    return trialsEachType


def find_trials_each_combination(parameter1,parameterPossibleValues1,parameter2,parameterPossibleValues2):
    '''
    Returns a boolean 3D array of size [nTrials,nValues1,nValues2]. True for each combination.
    '''
    if len(parameter1)!=len(parameter2):
        raise ValueError('parameters must be vectors of same size.')
    nTrials = len(parameter1)
    nValues1 = len(parameterPossibleValues1)
    nValues2 = len(parameterPossibleValues2)
    trialsEachComb = np.zeros((nTrials,nValues1,nValues2),dtype=bool)
    trialsEachType1 = find_trials_each_type(parameter1,parameterPossibleValues1)
    trialsEachType2 = find_trials_each_type(parameter2,parameterPossibleValues2)
    for ind2 in range(nValues2):
        trialsEachComb[:,:,ind2] = trialsEachType1 & trialsEachType2[:,ind2][:,np.newaxis]
    return trialsEachComb


'''
,validTrials=[]
    if(not len(validTrials)):
        validTrials = np.ones(nTrials,dtype=bool)
        trialsEachType[:,indval] = trialsThisValue & validTrials
'''

def find_trials_each_type_each_block(psyCurveParameter,psyCurveParameterPossibleValues,\
                                     currentBlock,currentBlockPossibleValues,validTrials=[]):
    '''
    Parameters
    ----------
    psyCurveParameter
    psyCurveParameterPossibleValues
    currentBlock
    currentBlockPossibleValues
    validTrials

    Returns
    -------
    trialsEachType: [nTrials,nParamValues,nBlockTypes] (boolean)

    See also:
    extracellpy.sessionanalysis.trials_by_condition()
    '''
    nTrials = len(psyCurveParameter)
    nValues = len(psyCurveParameterPossibleValues)
    nBlockTypes = len(currentBlockPossibleValues)
    if(not len(validTrials)):
        validTrials = np.ones(nTrials,dtype=bool)

    trialsEachBlock = np.zeros((nTrials,nBlockTypes),dtype=bool)
    for indb,blockID in enumerate(currentBlockPossibleValues):
        trialsEachBlock[:,indb] = (currentBlock==blockID)
    trialsEachType = np.zeros((nTrials,nValues,nBlockTypes),dtype=bool)
    for indval,paramValue in enumerate(psyCurveParameterPossibleValues):
        trialsThisValue = (psyCurveParameter==paramValue)
        for indb in range(nBlockTypes):
            trialsEachType[:,indval,indb] = trialsThisValue & \
                                            trialsEachBlock[:,indb] & validTrials

    return trialsEachType




def load_many_sessions(animalNames,sessions,paradigm='2afc',datesRange=None):
    '''
    Based on behavioranalysis.save_many_sessions_reversal()

    TO DO:
    - Add params='all', (it depends on loadbehavior.FlexCateg being able to load a subset of vars)
    - What to do if a parameter only exists for some sessions?
    '''
    if isinstance(animalNames,str):
        animalNames = [animalNames]
    if datesRange:
        datesLims = [parse_isodate(dateStr) for dateStr in datesRange]
        allDates = [datesLims[0]+datetime.timedelta(n) \
                        for n in range((datesLims[-1]-datesLims[0]).days+1)]
        allSessions = [oneDate.strftime('%Y%m%da') for oneDate in allDates]
    else:
        allSessions = sessions
    nAnimals = len(animalNames)
    if paradigm=='2afc':
        loadingClass = loadbehavior.FlexCategBehaviorData
    else:
        raise TypeError('Loading many sessions for that paradigm has not been implemented')

    #if params=='all':
    #    readmode = 'full'
    #else:
    #    readmode = params
    readmode = 'full'

    #allBehavData = {}
    #allBehavData['sessionID'] = np.empty(0,dtype='i2')
    #allBehavData['animalID'] = np.empty(0,dtype='i1')

    inds=0
    for inda,animalName in enumerate(animalNames):
        for indsa,thisSession in enumerate(allSessions):
            try:
                behavFile = loadbehavior.path_to_behavior_data(animalName,EXPERIMENTER,paradigm,thisSession)
                behavData = loadingClass(behavFile,readmode=readmode)
            except IOError:
                print thisSession+' does not exist'
                continue
            if inds==0:
                allBehavData = behavData  # FIXME: Should it be .copy()?
                nTrials = len(behavData['outcome']) # FIXME: what if this key does not exist?
                allBehavData['sessionID'] = np.zeros(nTrials,dtype='i2')
                allBehavData['animalID'] = np.zeros(nTrials,dtype='i1')
            else:
                for key,val in behavData.iteritems():
                    if not allBehavData.has_key(key):
                        allBehavData[key]=val
                    else:
                        allBehavData[key] = np.concatenate((allBehavData[key],val))
                nTrials = len(behavData['outcome']) # FIXME: what if this key does not exist?
                allBehavData['sessionID'] = np.concatenate((allBehavData['sessionID'],
                                                            np.tile(inds,nTrials)))
                allBehavData['animalID'] = np.concatenate((allBehavData['animalID'],
                                                            np.tile(inda,nTrials)))
            inds += 1
    return allBehavData


def behavior_summary(subjects,sessions,trialslim=[],outputDir='',paradigm=None,soundfreq=None):
    '''
    subjects: an array of animals to analyze (it can also be a string for a single animal)
    sessions: an array of sessions to analyze (it can also be a string for a single session)
    trialslim: array to set xlim() of dynamics' plot
    outputDir: where to save the figure (if not specified, nothing will be saved)
    paradigm: load data from a different paradigm. Warning: data should be loaded with
              loadbehavior.ReversalBehaviorData().
    '''
    if isinstance(subjects,str):
        subjects = [subjects]
    if isinstance(sessions,str):
        sessions = [sessions]
    nSessions = len(sessions)
    nAnimals = len(subjects)

    loadingClass = loadbehavior.FlexCategBehaviorData
    paradigm = '2afc'

    gs = gridspec.GridSpec(nSessions*nAnimals, 3)
    gs.update(hspace=0.5,wspace=0.4)
    plt.clf()
    for inds,thisSession in enumerate(sessions):
        for inda,animalName in enumerate(subjects):
            try:
                behavFile = loadbehavior.path_to_behavior_data(animalName,EXPERIMENTER,paradigm,thisSession)
                behavData = loadingClass(behavFile,readmode='full')
            except IOError:
                print thisSession+' does not exist'
                continue
            print 'Loaded %s %s'%(animalName,thisSession)

            # -- Plot either psychometric or average performance
            thisAnimalPos = 3*inda*nSessions
            thisPlotPos = thisAnimalPos+3*inds
            ax1=plt.subplot(gs[thisPlotPos])
            if any(behavData['psycurveMode']):
                (pline, pcaps, pbars, pdots) = plot_frequency_psycurve(behavData,fontsize=8)
                plt.setp(pdots,ms=6)
                plt.ylabel('% rightward')
                nValid = behavData['nValid'][-1]
                nTrials = len(behavData['nValid'])
                if soundfreq is None:
                    # freqsToUse = [behavData['lowFreq'][-1],behavData['highFreq'][-1]]
                    freqsToUse = [min(np.unique(behavData['targetFrequency'])),max(np.unique(behavData['targetFrequency']))]
                titleStr = '{0} [{1}] {2}\n'.format(behavData.session['subject'],behavData.session['date'],
                                                    behavData.session['hostname'])
                titleStr += '{0} valid, {1:.0%} early'.format(nValid,(nTrials-nValid)/float(nTrials))
                plt.title(titleStr,fontweight='bold',fontsize=8,y=0.95)
            else:
                behavData.find_trials_each_block()
                if soundfreq is None:
                    # freqsToUse = [behavData['lowFreq'][-1],behavData['highFreq'][-1]]
                    freqsToUse = [min(np.unique(behavData['targetFrequency'])),max(np.unique(behavData['targetFrequency']))]
                plot_summary(behavData,fontsize=8,soundfreq=freqsToUse)

            # -- Plot dynamics --
            ax2=plt.subplot(gs[thisPlotPos+1:thisPlotPos+3])
            plot_dynamics(behavData,winsize=40,fontsize=8,soundfreq=freqsToUse)
            #plt.setp(ax1.get_xticklabels(),visible=False)
            ax1xlabel = ax1.get_xlabel()
            ax2xlabel = ax2.get_xlabel()
            ax1.set_xlabel('')
            ax2.set_xlabel('')
            if trialslim:
                plt.xlim(trialslim)
            plt.draw()
            plt.show()
    plt.setp(ax1.get_xticklabels(),visible=True)
    plt.setp(ax2.get_xticklabels(),visible=True)
    ax1.set_xlabel(ax1xlabel)
    ax2.set_xlabel(ax2xlabel)
    #plt.draw()
    #plt.show()

    if len(outputDir):
        animalStr = '-'.join(subjects)
        sessionStr = '-'.join(sessions)
        # plt.gcf().set_size_inches((8.5,11))
        figformat = 'png' #'png' #'pdf' #'svg'
        filename = 'behavior_%s_%s.%s'%(animalStr,sessionStr,figformat)
        fullFileName = os.path.join(outputDir,filename)
        print 'saving figure to %s'%fullFileName
        plt.gcf().savefig(fullFileName,format=figformat)




def plot_summary(behavData,fontsize=12,soundfreq=None):
    '''
    Show summary of performance.
    First argument is an object created by loadbehavior.BehaviorData (or subclasses)
    '''
    correct = behavData['outcome']==behavData.labels['outcome']['correct']
    early = behavData['outcome']==behavData.labels['outcome']['invalid']
    #possibleFreq = np.unique(behavData['targetFrequency'])
    if soundfreq is None:
        possibleFreq = np.unique(behavData['targetFrequency'])
    else:
        possibleFreq = soundfreq
    possibleBlockID = np.unique(behavData['currentBlock'])
    trialsEachType = find_trials_each_type_each_block(behavData['targetFrequency'],possibleFreq,
                                                      behavData['currentBlock'],possibleBlockID)
    validTrialsEachType = trialsEachType & behavData['valid'][:,np.newaxis,np.newaxis].astype(bool)
    correctTrialsEachType = validTrialsEachType & correct[:,np.newaxis,np.newaxis]
    nCorrectEachType = np.sum(correctTrialsEachType,axis=0)
    nValidEachType = np.sum(validTrialsEachType,axis=0)

    #perfEachType = np.where(nValidEachType>0, nCorrectEachType/nValidEachType.astype(float), np.nan)
    perfEachType = nCorrectEachType/nValidEachType.astype(float)

    # --- Plot results ---
    itemsToPlot = nValidEachType.flatten()>0  #~np.isnan(perfEachType.flatten())
    perfToPlot = perfEachType.flatten()[itemsToPlot] # Show only 2 freq for each block type
    freqLabels = np.repeat(possibleFreq,len(possibleBlockID))[itemsToPlot]
    nValidCounts = nValidEachType.flatten()[itemsToPlot]
    xPos = [0,1,3,4][:len(perfToPlot)]
    ax = plt.gca()
    ax.set_xlim([-1,5])
    ax.set_ylim([0,100])
    plt.hold(True)
    hline50 = plt.axhline(50,linestyle=':',color='k',zorder=-1)
    hline75 = plt.axhline(75,linestyle=':',color='k',zorder=-1)
    hbars = plt.bar(xPos,100*perfToPlot,align='center',fc=[0.8,0.8,0.8],ec='k')
    for thispos,thistext in zip(xPos,nValidCounts):
        plt.text(thispos,10,str(thistext),ha='center',fontsize=fontsize)
    ax.set_ylabel('% correct',fontsize=fontsize)
    ax.set_xticks(xPos)
    ax.set_xticklabels(freqLabels/1000)

    titleStr = '{0} [{1}] {2}\n'.format(behavData.session['subject'],behavData.session['date'],
                                        behavData.session['hostname'])
    titleStr += '{0} valid, {1:.0%} early'.format(sum(nValidCounts),np.mean(early))
    ax.set_title(titleStr,fontweight='bold',fontsize=fontsize,y=0.95)
    ax.set_xlabel('Frequency (kHz)',fontsize=fontsize)
    extraplots.set_ticks_fontsize(ax,fontsize)
    plt.draw()
    plt.show()


def plot_frequency_psycurve(bdata,fontsize=12):
    '''
    Show psychometric curve (for frequency)
    '''
    targetFrequency = bdata['targetFrequency']
    choice=bdata['choice']
    valid=bdata['valid']& (choice!=bdata.labels['choice']['none'])
    choiceRight = choice==bdata.labels['choice']['right']
    possibleFreq = np.unique(targetFrequency)
    nFreq = len(possibleFreq)
    trialsEachFreq = find_trials_each_type(targetFrequency,possibleFreq)
    (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
       calculate_psychometric(choiceRight,targetFrequency,valid)
    (pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue,
                                                                ciHitsEachValue,xTickPeriod=1)
    plt.xlabel('Frequency (kHz)',fontsize=fontsize)
    plt.ylabel('Rightward trials (%)',fontsize=fontsize)
    extraplots.set_ticks_fontsize(plt.gca(),fontsize)
    return (pline, pcaps, pbars, pdots)

def plot_dynamics(behavData,winsize=40,fontsize=12,soundfreq=None):
    '''
    Plot performance in time for one session.
    First argument is an object created by loadbehavior.BehaviorData (or subclasses)
    '''
    ax = plt.gca()
    ax.cla()
    lineWidth = 2
    if not soundfreq:
        possibleFreq = np.unique(behavData['targetFrequency'])
    else:
        possibleFreq = soundfreq
    possibleColors = FREQCOLORS + ['k','m','c', 'b','r','g']
    colorEachFreq = dict(zip(possibleFreq,possibleColors))

    behavData.find_trials_each_block()

    nBlocks = behavData.blocks['nBlocks']
    trialsEachBlock = behavData.blocks['trialsEachBlock']
    validEachBlock = trialsEachBlock & (behavData['valid'][:,np.newaxis].astype(bool))
    nValidEachBlock = np.sum(validEachBlock,axis=0)
    lastValidEachBlock = np.cumsum(nValidEachBlock) # Actually, these values correspond to lastIndex+1
    firstValidEachBlock = np.concatenate(([0],lastValidEachBlock[:-1]))
    rightChoice = behavData['choice']==behavData.labels['choice']['right']

    hPlots = []
    plt.hold(True)
    for indb in range(nBlocks):
        trialsThisBlock = trialsEachBlock[:,indb]
        validThisBlock = validEachBlock[:,indb]
        for indf,thisFreq in enumerate(possibleFreq):
            thisColor = colorEachFreq[thisFreq]
            trialsThisFreq = (behavData['targetFrequency']==thisFreq)
            choiceVecThisFreq = np.ma.masked_array(rightChoice[validThisBlock])
            choiceVecThisFreq.mask = ~trialsThisFreq[validThisBlock]
            movAvChoice = extrafuncs.moving_average_masked(choiceVecThisFreq,winsize)
            hp, = plt.plot(range(firstValidEachBlock[indb],lastValidEachBlock[indb]),100*movAvChoice,
                           lw=lineWidth,color=thisColor)
            hPlots.append(hp)
    plt.ylim([-5,105])
    plt.axhline(50,color='0.5',ls='--')
    plt.ylabel('% rightward',fontsize=fontsize)
    plt.xlabel('Trial',fontsize=fontsize)
    extraplots.set_ticks_fontsize(ax,fontsize)
    plt.draw()
    plt.show()
    return hPlots

def calculate_psychometric(hitTrials,paramValueEachTrial,valid=None):
    '''
    Calculate fraction of hits for each parameter value (in vector param).
    hitTrials: (boolean array of size nTrials) hit or miss
    paramValueEachTrial: (array of size nTrials) parameter value for each trial
    valid: (boolean array of size nTrials) trials to use in calculation

    RETURNS:
    possibleValues: array with possible values of the parameter
    fractionHitsEachValue: array of same length as possibleValues
    ciHitsEachValue: array of size [2,len(possibleValues)]
    nTrialsEachValue: array of same length as possibleValues
    nHitsEachValue: array of same length as possibleValues
    '''
    try:
        from statsmodels.stats.proportion import proportion_confint #Used to compute confidence interval for the error bars.
        useCI = True
    except ImportError:
        print 'To calculate confidence intervals, please install "statsmodels" module.'
        useCI = False
    nTrials = len(hitTrials)
    if valid is None:
        valid = ones(nTrials,dtype=bool)
    possibleValues = np.unique(paramValueEachTrial)
    nValues = len(possibleValues)
    trialsEachValue = find_trials_each_type(paramValueEachTrial,possibleValues)

    nTrialsEachValue = np.empty(nValues,dtype=int)
    nHitsEachValue = np.empty(nValues,dtype=int)
    for indv,thisValue in enumerate(possibleValues):
        nTrialsEachValue[indv] = sum(valid & trialsEachValue[:,indv])
        nHitsEachValue[indv] = sum(valid & hitTrials & trialsEachValue[:,indv])

    fractionHitsEachValue = nHitsEachValue/nTrialsEachValue.astype(float)
    if useCI:
        ciHitsEachValue = np.array(proportion_confint(nHitsEachValue, nTrialsEachValue, method = 'wilson'))
    else:
        ciHitsEachValue = None
    return (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)

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

    bdata = load_many_sessions(animal, sessions)
    soundTypes = [bdata.labels['soundType'][x] for x in np.unique(bdata['soundType'])]

    dataObjs = []
    dataSoundTypes = {}

    for indType, thisType in enumerate(soundTypes):
        bdataThisType = load_many_sessions(animal, sessions)

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
            allBehavData = load_many_sessions(animalName, [session])
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
                    (pline, pcaps, pbars, pdots) = plot_frequency_psycurve(thisBehavData)
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
                    plot_summary(thisBehavData,fontsize=8,soundfreq=freqsToUse)
                    plt.title(soundType)

            #Plot the dynamics for all the sound types
            plt.subplot2grid((nAnimals*nSessions, nSoundTypes+2), (yInd, nSoundTypes), colspan=2)
            plot_dynamics(allBehavData, soundfreq = allFreqsToUse)
            plt.ylabel('')
            if trialslim:
                plt.xlim(trialslim)
            plt.title('{}, {}'.format(animalName, session))
            plt.subplots_adjust(hspace = 0.7)


## -- Deprecated code below -- ##

def OLD_calculate_psychometric(behavData,parameterName='targetFrequency'):
    '''
    FIXME: what to do about trials with no choice?
    It assumes behavData has the keys 'valid' and 'choice'.
    '''
    paramValues=bdata[parameterName]
    valid=bdata['valid']
    choice=bdata['choice']
    choiceRight = choice==bdata.labels['choice']['right']

    possibleValues = np.unique(paramValues)
    nValues = len(possibleValues)
    trialsEachValue = find_trials_each_type(paramValues,possibleValues)

    nTrialsEachValue = np.empty(nValues,dtype=int)
    nRightwardEachValue = np.empty(nValues,dtype=int)
    for indv,thisValue in enumerate(possibleValues):
        nTrialsEachValue[indv] = sum(valid & trialsEachValue[:,indv])
        nRightwardEachValue[indv] = sum(valid & choiceRight & trialsEachValue[:,indv])

    fractionRightEachValue = nRightwardEachValue/nTrialsEachValue.astype(float)
    confintervRightEachValue = [] # TO BE IMPLEMENTED LATER
    return (possibleValues,fractionRightEachValue,confintervRightEachValue,nTrialsEachValue,nRightwardEachValue)



def muscimol_plot_sound_type(animal, muscimolSessions, salineSessions, soundType, fontsize=12):

    '''
    DEPRECATED - this is a bad function
    Plot the average psycurve for muscimol sessions in red on top of the average saline psycurve in black.
    Psycurves are limited by the sound type.
    '''

    muscimolData = behavioranalysis.load_many_sessions(animal, muscimolSessions)

    trialsSoundTypeMus = muscimolData['soundType']==muscimolData.labels['soundType'][soundType]
    rightTrialsMus = (muscimolData['choice']==muscimolData.labels['choice']['right'])[trialsSoundTypeMus]
    freqEachTrialMus = muscimolData['targetFrequency'][trialsSoundTypeMus]
    validMus = muscimolData['valid'][trialsSoundTypeMus]


    (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
       calculate_psychometric(rightTrialsMus,freqEachTrialMus,validMus)
    (plineM, pcapsM, pbarsM, pdotsM) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue,
                                                                ciHitsEachValue,xTickPeriod=1)
    plt.xlabel('Frequency (kHz)',fontsize=fontsize)
    plt.ylabel('Rightward trials (%)',fontsize=fontsize)
    extraplots.set_ticks_fontsize(plt.gca(),fontsize)




    setp(plineM, color='r')
    setp(pcapsM, color='r')
    setp(pbarsM, color='r')
    setp(pdotsM, markerfacecolor='r')

    salineData = behavioranalysis.load_many_sessions(animal, salineSessions)

    trialsSoundTypeSal = salineData['soundType']==salineData.labels['soundType'][soundType]
    rightTrialsSal = (salineData['choice']==salineData.labels['choice']['right'])[trialsSoundTypeSal]
    freqEachTrialSal = salineData['targetFrequency'][trialsSoundTypeSal]
    validSal = salineData['valid'][trialsSoundTypeSal]


    (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
       calculate_psychometric(rightTrialsSal,freqEachTrialSal,validSal)
    (plineS, pcapsS, pbarsS, pdotsS) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue,
                                                                ciHitsEachValue,xTickPeriod=1)


    title("{}, {}".format(animal, soundType))

def plot_dynamics_sound_type(behavData, soundType, winsize=40,fontsize=12,soundfreq=None):
    '''
    DEPRECATED - load data into two data objects (one per sound type) and use the regular func
    Plot performance in time for one session.
    First argument is an object created by loadbehavior.BehaviorData (or subclasses)
    '''

    print 'FIXME: no removal of invalid trials in sound type dynamics'

    trialsSoundType = behavData['soundType']==behavData.labels['soundType'][soundType]

    valid = behavData['valid']
    validSoundType = valid[trialsSoundType]

    freqEachTrialSoundType = behavData['targetFrequency'][trialsSoundType]

    blockIDthisSoundType = behavData['currentBlock'][trialsSoundType]
    possibleBlockID = np.unique(blockIDthisSoundType)

    ax = plt.gca()
    ax.cla()
    lineWidth = 2

    if soundfreq is None:
        possibleFreq = [min(np.unique(freqEachTrialSoundType)), max(np.unique(freqEachTrialSoundType))]
    else:
        possibleFreq = soundfreq

    #########

    possibleColors = FREQCOLORS + ['k','m','c', 'b','r','g']
    colorEachFreq = dict(zip(possibleFreq,possibleColors))

    rightChoice = behavData['choice']==behavData.labels['choice']['right']
    rightChoiceSoundType = rightChoice[trialsSoundType]

    hPlots = []
    plt.hold(True)

    for indf,thisFreq in enumerate(possibleFreq):

        thisColor = colorEachFreq[thisFreq]
        trialsThisFreqSoundType = (freqEachTrialSoundType==thisFreq)

        choiceVecThisFreq = np.ma.masked_array(rightChoiceSoundType)
        choiceVecThisFreq.mask = ~trialsThisFreqSoundType

        movAvChoice = extrafuncs.moving_average_masked(choiceVecThisFreq,winsize)

        hp, = plt.plot(range(len(movAvChoice)), 100*movAvChoice,
                        lw=lineWidth,color=thisColor)
        hPlots.append(hp)

    plt.ylim([-5,105])
    plt.axhline(50,color='0.5',ls='--')
    plt.ylabel('% rightward',fontsize=fontsize)
    plt.xlabel('Trial',fontsize=fontsize)
    extraplots.set_ticks_fontsize(ax,fontsize)
    plt.draw()
    plt.show()
    return hPlots

def plot_summary_sound_type(behavData, soundType, foregroundColor=None, fontsize=12,soundfreq=None):
    '''
    DEPRECATED - using modswitching_report function now
    Show summary of performance.
    First argument is an object created by loadbehavior.BehaviorData (or subclasses)
    '''
    if foregroundColor is None:
        foregroundColor=[0.8,0.8,0.8]

    trialsSoundType = bdata['soundType']==bdata.labels['soundType'][soundType]
    choice = bdata['choice']
    targetFrequencySoundType = bdata['targetFrequency'][trialsSoundType]
    valid = bdata['valid']
    validSoundType = valid[trialsSoundType]
    correct = behavData['outcome']==behavData.labels['outcome']['correct']
    correctSoundType = correct[trialsSoundType]

    early = behavData['outcome']==behavData.labels['outcome']['invalid']
    earlySoundType = early[trialsSoundType]
    if soundfreq is None:
        targetFreqThisSoundType = behavData['targetFrequency'][trialsSoundType]
        possibleFreq = np.unique(targetFreqThisSoundType)
    else:
        possibleFreq = soundfreq

    blockIDthisSoundType = behavData['currentBlock'][trialsSoundType]
    possibleBlockID = np.unique(blockIDthisSoundType)
    trialsEachType = find_trials_each_type_each_block(targetFreqThisSoundType,possibleFreq,
                                                      blockIDthisSoundType,possibleBlockID)
    validTrialsEachType = trialsEachType & validSoundType[:,np.newaxis,np.newaxis].astype(bool)
    correctTrialsEachType = validTrialsEachType & correctSoundType[:,np.newaxis,np.newaxis]
    nCorrectEachType = np.sum(correctTrialsEachType,axis=0)
    nValidEachType = np.sum(validTrialsEachType,axis=0)

    #perfEachType = np.where(nValidEachType>0, nCorrectEachType/nValidEachType.astype(float), np.nan)
    perfEachType = nCorrectEachType/nValidEachType.astype(float)
    # --- Plot results ---
    itemsToPlot = nValidEachType.flatten()>0  #~np.isnan(perfEachType.flatten())
    perfToPlot = perfEachType.flatten()[itemsToPlot] # Show only 2 freq for each block type
    freqLabels = np.repeat(possibleFreq,len(possibleBlockID))[itemsToPlot]
    nValidCounts = nValidEachType.flatten()[itemsToPlot]
    xPos = [0,1,3,4][:len(perfToPlot)]
    ax = plt.gca()
    ax.set_xlim([-1,5])
    ax.set_ylim([0,100])
    plt.hold(True)
    hline50 = plt.axhline(50,linestyle=':',color='k',zorder=-1)
    hline75 = plt.axhline(75,linestyle=':',color='k',zorder=-1)
    hbars = plt.bar(xPos,100*perfToPlot,align='center',fc=foregroundColor,ec='k')
    for thispos,thistext in zip(xPos,nValidCounts):
        plt.text(thispos,10,str(thistext),ha='center',fontsize=fontsize)
    ax.set_ylabel('% correct',fontsize=fontsize)
    ax.set_xticks(xPos)
    if freqLabels[0]>=1000:
        ax.set_xticklabels(freqLabels/1000)
        ax.set_xlabel('Frequency (kHz)',fontsize=fontsize)
    else:
        ax.set_xticklabels(freqLabels)
        ax.set_xlabel('Frequency (Hz)',fontsize=fontsize)
    titleStr = '{0} [{1}] {2}\n'.format(behavData.session['subject'],behavData.session['date'],
                                        behavData.session['hostname'])
    titleStr += '{0} valid, {1:.0%} early'.format(sum(nValidCounts),np.mean(early))
    ax.set_title(titleStr,fontweight='bold',fontsize=fontsize,y=0.95)
    # ax.set_xlabel('Frequency (kHz)',fontsize=fontsize)
    extraplots.set_ticks_fontsize(ax,fontsize)
    plt.draw()
    plt.show()

def plot_frequency_psycurve_soundtype(bdata, soundType, fontsize=12):
    '''
    DEPRECATED
    Show psychometric curve (for any arbitrary sound type)
    '''

    trialsSoundType = bdata['soundType']==bdata.labels['soundType'][soundType]
    choice = bdata['choice']
    choiceRight = choice==bdata.labels['choice']['right']
    choiceRightSoundType = choiceRight[trialsSoundType]
    targetFrequencySoundType = bdata['targetFrequency'][trialsSoundType]
    valid = bdata['valid']
    validSoundType = valid[trialsSoundType]
    (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
        calculate_psychometric(choiceRightSoundType,targetFrequencySoundType,validSoundType)
    (pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,
                                                                fractionHitsEachValue,
                                                                ciHitsEachValue,
                                                                xTickPeriod=1)
    plt.xlabel('Frequency (kHz)',fontsize=fontsize)
    plt.ylabel('Rightward trials (%)',fontsize=fontsize)
    extraplots.set_ticks_fontsize(plt.gca(),fontsize)
    return (pline, pcaps, pbars, pdots)

def mod_switching_summary(animalName, sessions):

    fn = '/home/nick/data/behavior/nick/{0}/{1}_2afc_{2}.h5'.format(animalName, animalName, date)
    #fn = '/var/tmp/data/santiago/nick/nick_2afc_20160330a.h5' #Not psycurve

    bdata = loadbehavior.BehaviorData(fn)

    numSoundType = len(np.unique(bdata['soundType']))
    soundTypes = [bdata.labels['soundType'][np.unique(bdata['soundType'])[x]] for x in range(numSoundType)]

    plt.clf()
    if any(bdata['psycurveMode']):
        for indType, soundType in enumerate(soundTypes):
            plt.subplot2grid((numSoundType, 2),  (indType, 0))
            plot_frequency_psycurve_soundtype(bdata, soundType)
            plt.title('{}, {}'.format(animalName, soundType))

    else:
        for indType, soundType in enumerate(soundTypes):
            plt.subplot2grid((numSoundType, 2),  (indType, 0))
            plot_summary_sound_type(bdata, soundType)
            plt.title('{}, {}'.format(animalName, soundType))


    for indType, soundType in enumerate(soundTypes):
        plt.subplot2grid((numSoundType, 2),  (indType, 1))
        plot_dynamics_sound_type(bdata, soundType)
        plt.title('{}, {}'.format(animalName, soundType))

    behavFolder = '/home/nick/data/behavior_reports'
    figname = '{}_{}.png'.format(animalName, date)
    filename = os.path.join(behavFolder, figname)

    plt.suptitle(date)
    plt.tight_layout()
    plt.savefig(filename)

def percent_correct_sound_type(bdata, soundType):
    '''
    DEPRECATED
    Return the average percent correct for a behavior session, limited to a single sound type
    '''

    from statsmodels.stats.proportion import proportion_confint

    correctChoiceVec = bdata['outcome']==bdata.labels['outcome']['correct']
    trialsSoundType = bdata['soundType']==bdata.labels['soundType'][soundType]
    correctSoundType = correctChoiceVec[trialsSoundType]
    nRewardedSoundType = sum(correctSoundType)
    valid = bdata['valid']
    validSoundType = valid[trialsSoundType]
    nValidSoundType = sum(validSoundType)
    fractionCorrectSoundType = nRewardedSoundType/float(nValidSoundType)

    ci = np.array(proportion_confint(nRewardedSoundType, nValidSoundType, method = 'wilson'))

    return (fractionCorrectSoundType, nRewardedSoundType, nValidSoundType)

def overall_muscimol_performance(animal, muscimolSessions, salineSessions):

    '''
    DEPRECATED
    Plot psychometric and average performance reports for muscimol experiments
    INCOMPLETE: hard coded for chords and modulations right now. 
    '''

    #Plot the psycurves
    subplot(221)
    muscimol_plot_sound_type(animal, muscimolSessions, salineSessions, 'chords')

    subplot(223)
    muscimol_plot_sound_type(animal, muscimolSessions, salineSessions, 'amp_mod')


    #Overall muscimol and saline performance
    muscimolData = behavioranalysis.load_many_sessions(animal, muscimolSessions)
    muscimolChords = percent_correct_sound_type(muscimolData, 'chords')
    muscimolMod = percent_correct_sound_type(muscimolData, 'amp_mod')

    salineData = behavioranalysis.load_many_sessions(animal, salineSessions)
    salineChords = percent_correct_sound_type(salineData, 'chords')
    salineMod = percent_correct_sound_type(salineData, 'amp_mod')


    #Individual session muscimol and saline performance

    for indp, pair in enumerate(zip(salineSessions, muscimolSessions)):

        salineFile = loadbehavior.path_to_behavior_data(animal,settings.DEFAULT_EXPERIMENTER,'2afc',pair[0])
        salineData = loadbehavior.BehaviorData(salineFile,readmode='full')

        salineChords = percent_correct_sound_type(salineData, 'chords')
        salineMod = percent_correct_sound_type(salineData, 'amp_mod')

        muscimolFile = loadbehavior.path_to_behavior_data(animal,settings.DEFAULT_EXPERIMENTER,'2afc',pair[1])
        muscimolData = loadbehavior.BehaviorData(muscimolFile,readmode='full')

        muscimolChords = percent_correct_sound_type(muscimolData, 'chords')
        muscimolMod = percent_correct_sound_type(muscimolData, 'amp_mod')

        if indp==0:
            allPerfChords = array([salineChords, muscimolChords])
        else:
            allPerfChords = vstack([allPerfChords, array([salineChords, muscimolChords])])

        if indp==0:
            allPerfMod = array([salineMod, muscimolMod])
        else:
            allPerfMod = vstack([allPerfMod, array([salineMod, muscimolMod])])

    ## -- Chords performance
    subplot(222)
    bar([0, 1], [salineChords, muscimolChords], width=0.5, facecolor='w', edgecolor='k', linewidth = 2)
    #plot lines
    # for expt in allPerfChords:
    #     plot([0.25, 1.25], expt, '0.3', lw=2)

    #Plot points
    for point in allPerfChords[:,0]:
        plot(0.25, point, 'ko', ms=7)
    for point in allPerfChords[:,1]:
        plot(1.25, point, 'ro', ms=7)

    xlim([-0.5, 2])
    xticks([0.25, 1.25])
    ax = gca()
    ax.set_xticklabels(['Saline', 'Muscimol'])
    ylim([0, 100])
    ylabel('Percent Correct')

    ## -- Amp mod performance
    subplot(224)
    bar([0, 1], [salineMod, muscimolMod], width=0.5, facecolor='w', edgecolor='k', linewidth = 2)
    # for expt in allPerfMod:
    #     plot([0.25, 1.25], expt, '0.3', lw=2)

    #Plot points
    for point in allPerfMod[:,0]:
        plot(0.25, point, 'ko', ms=7)
    for point in allPerfMod[:,1]:
        plot(1.25, point, 'ro', ms=7)

    xlim([-0.5, 2])
    xticks([0.25, 1.25])
    ax = gca()
    ax.set_xticklabels(['Saline', 'Muscimol'])
    ylim([0, 100])
    ylabel('Percent Correct')

    return (allPerfChords, allPerfMod)

def plot_summary_sound_type(behavData, soundType, foregroundColor=None, fontsize=12,soundfreq=None):
    '''
    DEPRECATED
    Show summary of performance for one particular sound type
    First argument is an object created by loadbehavior.BehaviorData (or subclasses)
    '''
    if foregroundColor is None:
        foregroundColor=[0.8,0.8,0.8]

    trialsSoundType = behavData['soundType']==behavData.labels['soundType'][soundType]
    choice = behavData['choice']
    targetFrequencySoundType = behavData['targetFrequency'][trialsSoundType]
    valid = behavData['valid']
    validSoundType = valid[trialsSoundType]
    correct = behavData['outcome']==behavData.labels['outcome']['correct']
    correctSoundType = correct[trialsSoundType]

    early = behavData['outcome']==behavData.labels['outcome']['invalid']
    earlySoundType = early[trialsSoundType]
    if soundfreq is None:
        targetFreqThisSoundType = behavData['targetFrequency'][trialsSoundType]
        possibleFreq = np.unique(targetFreqThisSoundType)
    else:
        possibleFreq = soundfreq

    blockIDthisSoundType = behavData['currentBlock'][trialsSoundType]
    possibleBlockID = np.unique(blockIDthisSoundType)
    trialsEachType = find_trials_each_type_each_block(targetFreqThisSoundType,possibleFreq,
                                                      blockIDthisSoundType,possibleBlockID)
    validTrialsEachType = trialsEachType & validSoundType[:,np.newaxis,np.newaxis].astype(bool)
    correctTrialsEachType = validTrialsEachType & correctSoundType[:,np.newaxis,np.newaxis]
    nCorrectEachType = np.sum(correctTrialsEachType,axis=0)
    nValidEachType = np.sum(validTrialsEachType,axis=0)

    #perfEachType = np.where(nValidEachType>0, nCorrectEachType/nValidEachType.astype(float), np.nan)
    perfEachType = nCorrectEachType/nValidEachType.astype(float)
    # --- Plot results ---
    itemsToPlot = nValidEachType.flatten()>0  #~np.isnan(perfEachType.flatten())
    perfToPlot = perfEachType.flatten()[itemsToPlot] # Show only 2 freq for each block type
    freqLabels = np.repeat(possibleFreq,len(possibleBlockID))[itemsToPlot]
    nValidCounts = nValidEachType.flatten()[itemsToPlot]
    xPos = [0,1,3,4][:len(perfToPlot)]
    ax = plt.gca()
    ax.set_xlim([-1,5])
    ax.set_ylim([0,100])
    plt.hold(True)
    hline50 = plt.axhline(50,linestyle=':',color='k',zorder=-1)
    hline75 = plt.axhline(75,linestyle=':',color='k',zorder=-1)
    hbars = plt.bar(xPos,100*perfToPlot,align='center',fc=foregroundColor,ec='k')
    for thispos,thistext in zip(xPos,nValidCounts):
        plt.text(thispos,10,str(thistext),ha='center',fontsize=fontsize)
    ax.set_ylabel('% correct',fontsize=fontsize)
    ax.set_xticks(xPos)
    if freqLabels[0]>=1000:
        ax.set_xticklabels(freqLabels/1000)
        ax.set_xlabel('Frequency (kHz)',fontsize=fontsize)
    else:
        ax.set_xticklabels(freqLabels)
        ax.set_xlabel('Frequency (Hz)',fontsize=fontsize)
    titleStr = '{0} [{1}] {2}\n'.format(behavData.session['subject'],behavData.session['date'],
                                        behavData.session['hostname'])
    titleStr += '{0} valid, {1:.0%} early'.format(sum(nValidCounts),np.mean(early))
    ax.set_title(titleStr,fontweight='bold',fontsize=fontsize,y=0.95)
    # ax.set_xlabel('Frequency (kHz)',fontsize=fontsize)
    extraplots.set_ticks_fontsize(ax,fontsize)
    plt.draw()
    plt.show()

if __name__ == "__main__":

    CASE=6
    if CASE==1:
        from jaratoolbox import loadbehavior
        import numpy as np
        experimenter = 'santiago'
        paradigm = '2afc'
        subject = 'test020'
        session = '20140421a'

        behavFile = loadbehavior.path_to_behavior_data(subject,experimenter,paradigm,session)
        behavData = loadbehavior.FlexCategBehaviorData(behavFile,readmode='full')
        behavData.find_trials_each_block()

        #trialsEachBlock = behavData.blocks['trialsEachBlock']
        #nValidEachBlock = np.sum(trialsEachBlock & (~behavData['valid'][:,np.newaxis]),axis=0)
        #validEachBlock = trialsEachBlock & behavData['valid'][:,np.newaxis].astype(bool)

        #plot_dynamics(behavData,winsize=100)
        plot_summary(behavData)
        #tet = find_trials_each_type(behavData['targetFrequency'],np.unique(behavData['targetFrequency']),
        #                            behavData['currentBlock'],np.unique(behavData['currentBlock']))

    elif CASE==2:
        if 1:
            subjects = ['test011','test012','test013','test014','test015',
                        'test016','test017','test018','test019','test020']
        else:
            subjects = ['test050','test051','test052','test053','test054',
                        'test055','test056','test057','test058','test059']
        #subjects = ['test019','test020']
        #sessions = '20140321a' # No currentBlock
        sessions = '20140616a'
        behavior_summary(subjects,sessions,trialslim=[0,1200],outputDir='/tmp/')

    elif CASE==3:
        fname=loadbehavior.path_to_behavior_data('test052','santiago','2afc','20140911a')
        bdata=loadbehavior.BehaviorData(fname)
        (possibleFreq,pRightEach,ci,nTrialsEach,nRightwardEach) = OLD_calculate_psychometric(bdata,
                                                                                         parameterName='targetFrequency')
        print pRightEach
    elif CASE==4:
        allBehavData = load_many_sessions(['test020'],sessions=['20140421a','20140422a','20140423a'])
    elif CASE==5:
        param = np.array([7,4,7,5,7,4,7,5,7,4,7,8,8,8])
        possibleParam = np.unique(param)
        tet = find_trials_each_type(param,possibleParam)
        mask = param>4
        tet = tet & mask[:,np.newaxis]
        print possibleParam
        print tet
    elif CASE==6:
        #parameter1 = np.array([1,2,3,4,5,1,2,3,4,5])
        #parameter2 = np.array([2,2,2,3,3,3,4,4,4,4])
        parameter1 = np.array([1,2,1,2])
        parameter2 = np.array([4,4,5,6])
        tet = find_trials_each_combination(parameter1,np.unique(parameter1),parameter2,np.unique(parameter2))
        print tet
