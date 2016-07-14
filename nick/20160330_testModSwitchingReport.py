from jaratoolbox import loadbehavior
from jaratoolbox.test.nick import behavioranalysis_vnick as behavioranalysis
from jaratoolbox.test.nick.behavioranalysis_vnick import *
from jaratoolbox import extraplots
from jaratoolbox import colorpalette

fn = '/var/tmp/data/santiago/test/test_2afc_20160331a.h5'
#fn = '/var/tmp/data/santiago/nick/nick_2afc_20160330a.h5' #Not psycurve
bdata = loadbehavior.BehaviorData(fn)

trialsAmpMod = bdata['soundType']==bdata.labels['soundType']['amp_mod']
trialsTones = bdata['soundType']==bdata.labels['soundType']['tones']

choice = bdata['choice']
choiceRight = choice==bdata.labels['choice']['right']

choiceRightAmpMod = choiceRight[trialsAmpMod]
choiceRightTones = choiceRight[trialsTones]

targetFrequencyAmpMod = bdata['targetFrequency'][trialsAmpMod]
targetFrequencyTones = bdata['targetFrequency'][trialsTones]

valid = bdata['valid']
validAmpMod = valid[trialsAmpMod]
validTones = valid[trialsTones]

#Tones
figure()
(possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
    behavioranalysis.calculate_psychometric(choiceRightTones,targetFrequencyTones,validTones)

(pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,
                                                            fractionHitsEachValue,
                                                            ciHitsEachValue,
                                                            xTickPeriod=1)



#Amp Mod
figure()
(possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
    behavioranalysis.calculate_psychometric(choiceRightAmpMod,targetFrequencyAmpMod,validAmpMod)

(pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,
                                                            fractionHitsEachValue,
                                                            ciHitsEachValue,
                                                            xTickPeriod=1)




def plot_frequency_psycurve_soundtype(bdata, soundType, fontsize=12):
    '''
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
        behavioranalysis.calculate_psychometric(choiceRightSoundType,targetFrequencySoundType,validSoundType)
    (pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,
                                                                fractionHitsEachValue,
                                                                ciHitsEachValue,
                                                                xTickPeriod=1)
    plt.xlabel('Frequency (kHz)',fontsize=fontsize)
    plt.ylabel('Rightward trials (%)',fontsize=fontsize)
    extraplots.set_ticks_fontsize(plt.gca(),fontsize)
    return (pline, pcaps, pbars, pdots)




fn= '/home/nick/data/behavior/nick/amod004/amod004_2afc_20160408a.h5'
#fn = '/var/tmp/data/santiago/nick/nick_2afc_20160330a.h5' #Not psycurve
bdata = loadbehavior.BehaviorData(fn)


# figure()
# plot_frequency_psycurve_soundtype(bdata, 'amp_mod')
# title('amod002, amp_mod')
figure()
plot_summary_sound_type(bdata, 'amp_mod')
title('amod004, amp_mod')

# figure()
# plot_frequency_psycurve_soundtype(bdata, 'chords')
# title('amod002, chords')
figure()
plot_summary_sound_type(bdata, 'chords')
title('amod004, chords')





fn = '/home/nick/data/behavior/nick/amod002/amod002_2afc_20160401a.h5'
bdata = loadbehavior.BehaviorData(fn)

figure()
plot_frequency_psycurve_soundtype(bdata, 'amp_mod')
title('amod003, amp_mod')
# figure()
# plot_summary_sound_type(bdata, 'amp_mod')
# title('amod003, amp_mod')

figure()
plot_frequency_psycurve_soundtype(bdata, 'tones')
title('amod003, tones')
# figure()
# plot_summary_sound_type(bdata, 'tones')
# title('amod003, tones')


#Test summary plot

fn = '/var/tmp/data/santiago/nick/nick_2afc_20160330a.h5' #Not psycurve
bdata = loadbehavior.BehaviorData(fn)


def plot_summary_sound_type(behavData, soundType, foregroundColor=None, fontsize=12,soundfreq=None):
    '''
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

figure()
plot_summary_sound_type(bdata, 'amp_mod', colorpalette.TangoPalette['SkyBlue1'])

figure()
plot_summary_sound_type(bdata, 'tones', colorpalette.TangoPalette['Chameleon2'])



def plot_dynamics_sound_type(behavData, soundType, winsize=40,fontsize=12,soundfreq=None):
    '''
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
        targetFreqThisSoundType = behavData['targetFrequency'][trialsSoundType]
        possibleFreq = np.unique(targetFreqThisSoundType)
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
        # import ipdb; ipdb.set_trace()
        hPlots.append(hp)

    plt.ylim([-5,105])
    plt.axhline(50,color='0.5',ls='--')
    plt.ylabel('% rightward',fontsize=fontsize)
    plt.xlabel('Trial',fontsize=fontsize)
    extraplots.set_ticks_fontsize(ax,fontsize)
    plt.draw()
    plt.show()
    return hPlots





fn = '/home/nick/data/behavior/nick/amod004/amod004_2afc_20160409a.h5'
#fn = '/var/tmp/data/santiago/nick/nick_2afc_20160330a.h5' #Not psycurve

figure()
plot_dynamics_sound_type(bdata, 'chords', soundfreq=[5000, 16000])
title('amod004, chords')

figure()
plot_dynamics_sound_type(bdata, 'amp_mod', soundfreq=[8, 64])
title('amod004, amp_mod')




#DEBUGGING

fn = '/var/tmp/data/santiago/nick/nick_2afc_20160330a.h5' #Not psycurve
bdata = loadbehavior.FlexCategBehaviorData(fn)

soundType = 'amp_mod'
behavData=bdata

trialsSoundType = behavData['soundType']==behavData.labels['soundType'][soundType]
choice = behavData['choice']

#FIXME: I am tempted to ignore invalid trials for now...
valid = behavData['valid']
validSoundType = valid[trialsSoundType]

choiceRight = choice==bdata.labels['choice']['right']
choiceRightSoundType = choiceRight[trialsSoundType]


early = behavData['outcome']==behavData.labels['outcome']['invalid']
earlySoundType = early[trialsSoundType]

blockIDthisSoundType = behavData['currentBlock'][trialsSoundType]
possibleBlockID = np.unique(blockIDthisSoundType)

ax = plt.gca()
ax.cla()
lineWidth = 2

targetFreqThisSoundType = behavData['targetFrequency'][trialsSoundType]

#Just do 2 frequencies, lowest and highest
possibleFreq = np.unique(targetFreqThisSoundType)
possibleFreq = possibleFreq[array([0, -1])]

#########

# behavData.find_trials_each_block()

# nBlocks = behavData.blocks['nBlocks']

# trialsEachBlock = behavData.blocks['trialsEachBlock']

# validEachBlock = trialsEachBlock & (behavData['valid'][:,np.newaxis].astype(bool))
# nValidEachBlock = np.sum(validEachBlock,axis=0)
# lastValidEachBlock = np.cumsum(nValidEachBlock) # Actually, these values correspond to lastIndex+1
# firstValidEachBlock = np.concatenate(([0],lastValidEachBlock[:-1]))
# rightChoice = behavData['choice']==behavData.labels['choice']['right']

# for indb in range(nBlocks):
#     trialsThisBlock = trialsEachBlock[:,indb]
#     validThisBlock = validEachBlock[:,indb]
#     for indf,thisFreq in enumerate(possibleFreq)
#         choiceVecThisFreq = np.ma.masked_array(rightChoice[validThisBlock])
#         choiceVecThisFreq.mask = ~trialsThisFreq[validThisBlock]
#         movAvChoice = extrafuncs.moving_average_masked(choiceVecThisFreq,winsize)
#         hp, = plt.plot(range(firstValidEachBlock[indb],lastValidEachBlock[indb]),100*movAvChoice,
#                         lw=lineWidth,color=thisColor)
#         hPlots.append(hp)


possibleColors = FREQCOLORS + ['k','m','c', 'b','r','g']
colorEachFreq = dict(zip(possibleFreq,possibleColors))
hPlots = []
plt.hold(True)
winsize=40
lineWidth=2
for indf,thisFreq in enumerate(possibleFreq)
    thisColor = colorEachFreq[thisFreq]
    trialsThisFreq = (targetFreqThisSoundType==thisFreq)
    choiceVecThisFreq = choiceRightSoundType[trialsThisFreq]
    movAvChoice = extrafuncs.moving_average_masked(choiceVecThisFreq,winsize)
    hp, = plt.plot(range(0, len(targetFreqThisSoundType)),100*movAvChoice,
                    lw=lineWidth,color=thisColor)
    hPlots.append(hp)


plt.ylim([-5,105])
plt.axhline(50,color='0.5',ls='--')
plt.ylabel('% rightward',fontsize=fontsize)
plt.xlabel('Trial',fontsize=fontsize)
extraplots.set_ticks_fontsize(ax,fontsize)
plt.draw()
plt.show()
