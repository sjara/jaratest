'''
Script to load many behavior sessions and generate summary(average) psychometric curve for photostim_freq_discri paradigm by trialType.
Lan Guo 20160608
'''
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
#from jaratest.lan import behavioranalysis_vlan as behavioranalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import extraplots
from jaratoolbox import loadbehavior
from jaratoolbox import settings
from jaratoolbox import colorpalette



def plot_ave_choice_n_reaction_time(animal,session,trialLimit=None):
    '''
    Arguments:
    animal is a string of the animal name you want to plot.
    session is a list of behavior session names(strings) you want to plot.
    trialLimit is an optional parameter, should be a list of integers giving the beginning and end of trials numbers you want to plot.
    '''

    FREQCOLORS = [colorpalette.TangoPalette['Chameleon3'],
                  colorpalette.TangoPalette['ScarletRed1'],
                  colorpalette.TangoPalette['SkyBlue2'] , 'g', 'm', 'k']

    allBehavDataThisAnimal = behavioranalysis.load_many_sessions(animal,session) #This is lazy, should use loadbehavior module instead
    targetFrequency = allBehavDataThisAnimal['targetFrequency']
    choice = allBehavDataThisAnimal['choice']
    valid=allBehavDataThisAnimal['valid']& (choice!=allBehavDataThisAnimal.labels['choice']['none'])
    if trialLimit:
        trialSelector = np.zeros(len(valid),dtype=bool)
        trialSelector[trialLimit[0]:trialLimit[1]] = True
    else:
        trialSelector = np.ones(len(valid),dtype=bool)
    valid = (valid & trialSelector)
    #print sum(trialSelector), sum(valid)
    
    #choiceRight = choice==allBehavDataThisAnimal.labels['choice']['right']
    timeCenterOut=allBehavDataThisAnimal['timeCenterOut']
    if np.all(np.isnan(timeCenterOut)):
        timeCenterOut = calculate_center_out_times(animal,session)
    else:
        reactionTime = timeCenterOut-allBehavDataThisAnimal['timeTarget']-0.1 # Time it takes to initiate action after sound
        choiceTime = allBehavDataThisAnimal['timeSideIn']-timeCenterOut  # Time it takes to get to side port after leaving center port; value is NaN in invalid trials
    
    timeDf = pd.DataFrame()
    timeDf['valid'] = valid
    timeDf['choice'] = choice #For choice:0=left;1=right;2=none
    timeDf['type_of_stim'] = allBehavDataThisAnimal['trialType'] #0=no_laser;1=left_laser;2=right_laser
    timeDf['reactionTime'] = reactionTime
    timeDf['choiceTime'] = choiceTime
    timeDf['choiceTime'][np.isnan(choiceTime)] = 0

    import seaborn as sns
    g = sns.FacetGrid(timeDf, row='choice', col='type_of_stim', margin_titles=True)
    g.map(dot_plot_w_mean_std_by_category,'reactionTime','choiceTime').set(xlim=(0.5,2.5),ylim=(-0.05,1.05),xticks=[1,2],xticklabels=['Reaction time','Choice time'],xlabel='',ylabel='Time (sec)')
    print timeDf.head(20)
    plt.suptitle('%s_%s reaction and choice time plot'%(animal,session))   
    #if len(sessions)==1:
    #    plt.suptitle('%s_%s reaction and choice time plot' %(animal,sessions[0]),fontsize=8)
    #else:
    #    plt.suptitle('%s_%sto%s reaction and choice time plot'%(animal,sessions[0],sessions[-1]),fontsize=8)   
    plt.tight_layout()
    plt.show()


def dot_plot_w_mean_std_by_category(y1,y2,**kwargs):
    '''
    Given two columns in a dataframe with each row containing paired observations, generate dot plot for each category.
    '''
    import numpy as np
    ax = plt.gca()
    nObservations = len(y1)
    x1 = 1 + (np.random.random(nObservations)-0.5)/5
    y1 = y1.values
    y1Mean = np.mean(y1)
    e1 = np.std(y1)
    ax.plot(x1,y1,'o',ms=2)
    ax.errorbar(1.3,y1Mean,yerr=e1,linestyle='None', marker='o',ms=8,color='k',ecolor='k',capthick=2,elinewidth=3)
    x2 = 2 + (np.random.random(nObservations)-0.5)/5
    y2 = y2.values
    y2Mean = np.mean(y2)
    e2 = np.std(y2)
    ax.plot(x2,y2,'o',ms=2)
    ax.errorbar(1.7,y2Mean,yerr=e2,linestyle='None', marker='o',ms=8,color='k',ecolor='k',capthick=2,elinewidth=3)

     
def save_figure(animal,session,figformat='png'):
    outputDir='/home/languo/data/behavior_reports' 
    #animalStr = animal
    #sessionStr = session
    filename = '%s_%s_reaction_choice_times.%s'%(animal,session,figformat)
    fullFileName = os.path.join(outputDir,filename)
    print 'saving figure to %s'%fullFileName
    plt.gcf().savefig(fullFileName,format=figformat)


if __name__ == '__main__':
    animals = ['d1pi014']

    if len(sys.argv)>1:
        sessions = sys.argv[1:]

    #nSessions = len(sessions)
    #nAnimals = len(subjects)
    #gs = gridspec.GridSpec(nAnimals, 3)
    #gs = gridspec.GridSpec(nAnimals,1)
    #gs.update(hspace=0.5,wspace=0.4)

    for inda, thisAnimal in enumerate(animals):
        for session in sessions:
            plot_ave_choice_n_reaction_time(thisAnimal,[session])
            plt.show()
            save_figure(thisAnimal,session)

