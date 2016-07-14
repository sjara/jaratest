
from jaratoolbox import behavioranalysis
from jaratoolbox import loadbehavior
import numpy as np
from pylab import *
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportion_confint #Used to compute confidence interval for the error bars. 
from jaratoolbox import settings 

subjects = ['hm4d004', 'hm4d005', 'hm4d006']
session = '20140826a'

#This can handle up to 9 subjects now but there could be a more robust solution
#FIXME: May need to change positions so they make more visual sense
if len(subjects)==1:
    positions = [(0,0)]
    shape = (1, 1)
elif len(subjects)==2:
    positions = [(0,0), (1, 0)]
    shape = (2, 1)
elif len(subjects)>2 and len(subjects)<=4:
    positions=[(0,0), (0,1), (1,0), (1,1)]
    shape=(2,2)
elif len(subjects)>4 and len(subjects)<=6:
    positions=[(0,0), (0,1), (1,0), (1,1), (2, 0), (2, 1)]
    shape = (3, 2)
elif len(subjects)>6 and len(subjects)<=9:
    positions=[(0,0), (0,1), (1,0), (1,1), (2, 0), (2, 1), (0, 2), (1, 2), (2, 2)]
    shape = (3,3) 
    
else:
    print "This function accepts up to 9 subjects"
    break

for ind, subject in enumerate(subjects): #Iterate through each subject
    fname=loadbehavior.path_to_behavior_data(subject,'nick','2afc',session)

    try: #Attempt to load the data for this subject

        bdata=loadbehavior.BehaviorData(fname)

    except IOError: #If the data from this subject is not available:
        
        ax1=plt.subplot2grid(shape, positions[ind]) #Alert the user
        xlim([0,2])
        ylim([0,2])
        ax1.text(1, 1, "No Data Available", va = 'center', ha = 'center', color = 'r')
        title(subject)
        continue #Continue to the next subject
    
    #Extract data from the bdata object
    targetFrequency=bdata['targetFrequency']
    valid=bdata['valid']
    choice=bdata['choice']
    intensities=bdata['targetIntensity']
    choiceRight = choice==bdata.labels['choice']['right']

    #Find trials at each frequency
    possibleFreq = np.unique(targetFrequency)
    nFreq = len(possibleFreq) 
    trialsEachFreq = behavioranalysis.find_trials_each_type(targetFrequency,possibleFreq)

    #Preallocate arrays
    fractionRightEachFreq=np.empty(nFreq)
    confLimitsEachFreq=np.empty([2, nFreq]) #Upper and lower confidence limits
    nTrialsEachFreq = np.empty(nFreq)
    nRightwardEachFreq = np.empty(nFreq)

    #Configure subplot for this subject
    ax1=plt.subplot2grid(shape, positions[ind])
    
    #Compute the number right and c.i for each freq.
    for indf,thisFreq in enumerate(possibleFreq): 

        nTrialsThisFreq = sum(valid & trialsEachFreq[:,indf])
        nRightwardThisFreq =  sum(valid & choiceRight & trialsEachFreq[:,indf])
        conf = np.array(proportion_confint(nRightwardThisFreq, nTrialsThisFreq, method = 'wilson'))
        
        nTrialsEachFreq[indf] = nTrialsThisFreq
        nRightwardEachFreq[indf] = nRightwardThisFreq
        confLimitsEachFreq[0, indf] = conf[0] # Lower ci
        confLimitsEachFreq[1, indf] = conf[1] # Upper ci

    #Compute %right (c.i. are already in percent)
    fractionRightEachFreq = nRightwardEachFreq/nTrialsEachFreq.astype(float)

    #plot(possibleFreq,fractionRightEachFreq,'-o')
    #gca().set_xscale('log')

    #Find lengths of whiskers for plotting function
    upperWhisker = confLimitsEachFreq[1, :] - fractionRightEachFreq
    lowerWhisker = fractionRightEachFreq - confLimitsEachFreq[0,:]
    
    #Plot the data for this subject
    x = range(nFreq)
    errorbar(x, fractionRightEachFreq, yerr = [lowerWhisker, upperWhisker])
    axhline(y=0.5, color = 'red')
    title(subject)
    ylim([0,1])
    
#Include the date of the session
suptitle(session)
show()


'''
    fractionRightEachFreq = nRightwardEachFreq/nTrialsEachFreq.astype(float)

    #plot(possibleFreq,fractionRightEachFreq,'-o')
    #gca().set_xscale('log')
    positions=[(0,0), (0,1), (1,0), (1,1)]
    ax1=plt.subplot2grid((2,2), positions[ind])
    ax1.plot(fractionRightEachFreq,'-o')
    title(subject)
    ylim([0,1])
show()
'''
