'''
Tools for analyzing behavioral data.
'''

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import extrafuncs
from jaratoolbox import extraplots
from jaratoolbox import loadbehavior
from jaratoolbox import settings as settings
reload(settings)
from jaratoolbox import colorpalette

EXPERIMENTER = settings.DEFAULT_EXPERIMENTER
FREQCOLORS = [colorpalette.TangoPalette['Chameleon3'],
              colorpalette.TangoPalette['ScarletRed1'],
              colorpalette.TangoPalette['SkyBlue2'] ]
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
                    freqsToUse = [behavData['lowFreq'][-1],behavData['highFreq'][-1]]
                titleStr = '{0} [{1}] {2}\n'.format(behavData.session['subject'],behavData.session['date'],
                                                    behavData.session['hostname'])
                titleStr += '{0} valid, {1:.0%} early'.format(nValid,(nTrials-nValid)/float(nTrials))
                plt.title(titleStr,fontweight='bold',fontsize=8,y=0.95)
            else:
                behavData.find_trials_each_block()
                if soundfreq is None:
                    freqsToUse = [behavData['lowFreq'][-1],behavData['highFreq'][-1]]
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
        plt.gcf().set_size_inches((8.5,11))
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
