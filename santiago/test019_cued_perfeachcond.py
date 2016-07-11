'''
Show performance for each condition in cued task
'''


from jaratoolbox import behavioranalysis
from pylab import *
from jaratoolbox import loadbehavior
from jaratoolbox import extraplots
import sys
import os

if len(sys.argv)>1:
    session = sys.argv[1]+'a'
else:
    session = '20150329a'

subjects = ['cued001','cued002','cued003','cued004','cued005','cued006']
#subjects = ['cued004']
nAnimals = len(subjects)

smallFontSize = 8
fontSize = 10



clf()
for inda,animalName in enumerate(subjects):
    fname = loadbehavior.path_to_behavior_data(animalName,'santiago','2afc',session)
    try:
        bdata=loadbehavior.BehaviorData(fname)
    except IOError:
        #print fname+' does not exist'
        continue

    nReward = bdata['nRewarded'][-1]
    nValid = bdata['nValid'][-1]
    fractionCorrect = nReward/float(nValid)

    targetFrequency = bdata['targetFrequency']
    possibleTarget = unique(targetFrequency)
    cueFrequency = bdata['cueFrequency']
    possibleCue = unique(cueFrequency)

    trialsEachTarget = behavioranalysis.find_trials_each_type(targetFrequency,possibleTarget)
    trialsEachCue = behavioranalysis.find_trials_each_type(cueFrequency,possibleCue)

    correct = bdata['outcome']==(bdata.labels['outcome']['correct'])

    correctEachTarget = trialsEachTarget & correct[:,np.newaxis] 
    nTrialsEachTarget = trialsEachTarget.sum(axis=0)
    nCorrectEachTarget = correctEachTarget.sum(axis=0)
    fractionCorrectEachTarget = nCorrectEachTarget.astype(float)/nTrialsEachTarget

    correctEachCue = trialsEachCue & correct[:,np.newaxis] 
    nTrialsEachCue = trialsEachCue.sum(axis=0)
    nCorrectEachCue = correctEachCue.sum(axis=0)
    fractionCorrectEachCue = nCorrectEachCue.astype(float)/nTrialsEachCue

    ax0 = subplot2grid((nAnimals,3),(inda, 0))
    axhline(50,ls='--',color='0.6')
    axhline(75,ls='--',color='0.8')
    plot(100*fractionCorrectEachTarget,'ob-',mec='none')
    ylim([0,100])
    xlim([-0.5,len(possibleTarget)-0.5])
    ylabel(animalName+'\nCorrect (%)',fontsize=fontSize)
    if inda==nAnimals-1:
        xlabel('Target frequency',fontsize=fontSize)

    ax1 = subplot2grid((nAnimals,3),(inda, 1))
    axhline(50,ls='--',color='0.6')
    axhline(75,ls='--',color='0.8')
    plot(100*fractionCorrectEachCue,'og-',mec='none')
    ylim([0,100])
    xlim([-0.5,len(possibleCue)-0.5])
    #ylabel('Correct (%)',fontsize=fontSize)
    if inda==nAnimals-1:
        xlabel('Cue frequency',fontsize=fontSize)
    if inda==0:
        title(session)
    
    tec = behavioranalysis.find_trials_each_combination(targetFrequency,possibleTarget,cueFrequency,possibleCue)
    nTrialsEachComb = tec.sum(axis=0)
    nCorrectEachComb = np.sum(tec & correct[:,np.newaxis,np.newaxis],axis=0)
    fractionCorrectEachComb = nCorrectEachComb.astype(float)/nTrialsEachComb
    ax2 = subplot2grid((nAnimals,3),(inda, 2))
    if 1:
        imshow(100*fractionCorrectEachComb,cmap='PiYG',vmin=0,vmax=100)
        cbar = colorbar()
        cbar.set_ticks([0,25,50,75,100])
        cbar.set_label('Correct (%)', rotation=270, fontsize=fontSize)
        plt.setp(cbar.ax.get_yticklabels(),fontsize=smallFontSize)
    else:
        imshow(nTrialsEachComb,cmap='jet',vmin=0)
        cbar = colorbar()
    for indt in range(len(possibleTarget)):
        for indc in range(len(possibleCue)):
            text(indc,indt,nTrialsEachComb[indt,indc],ha='center',va='center',fontsize=8,color='k')

    ylabel('Target frequency',fontsize=fontSize)
    if inda==nAnimals-1:
        xlabel('Cue frequency',fontsize=fontSize)
    ax2.set_xticks(range(len(possibleCue)))
    ax2.set_yticks(range(len(possibleTarget)))

    extraplots.set_ticks_fontsize(ax0, smallFontSize)
    extraplots.set_ticks_fontsize(ax1, smallFontSize)
    extraplots.set_ticks_fontsize(ax2, smallFontSize)
    show()

PRINT_FIG=1
outputDir = '/var/tmp/cuedbehavior_reports/'
if PRINT_FIG:
    animalStr = '-'.join(subjects)
    #sessionStr = '-'.join(sessions)
    sessionStr = session
    plt.gcf().set_size_inches((8.5,11))
    figformat = 'png' #'png' #'pdf' #'svg'
    filename = 'cuedbehavior_%s_%s.%s'%(animalStr,sessionStr,figformat)
    fullFileName = os.path.join(outputDir,filename)
    print 'saving figure to %s'%fullFileName
    plt.gcf().savefig(fullFileName,format=figformat)



'''

m=np.vstack((bdata['cueFrequency'],bdata['targetFrequency'],bdata['rewardSide'],bdata['choice'],bdata['outcome'])).T
print m[:20,:]

'''
