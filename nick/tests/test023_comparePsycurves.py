'''
Author: Nick Ponvert
2014-11-18

Comparing two proportions, assuming approximately normal distribution (this might not be the way to go)

import numpy as np
from scipy.stats import norm
success1 = 351.0
trials1 = 605.0

success2 = 41.0
trials2 = 195.0

#Do these proportions differ?

phat1 = success1/trials1
phat2 = success2/trials2
phat = (success1 + success2)/(trials1 + trials2)

hyp_0_difference = 0

zscore = ((phat1 - phat2) - hyp_0_difference)/np.sqrt(phat *(1-phat)*(1/trials1 + 1/trials2))

p_val = norm.sf(zscore)*2 #Two-sided test

#print p_val
'''

#IMPORTANT: This script assumes that both behavior sessions were conducted using the same paradigm (same number of freqs)
#Also, the comparison assumes that the differences between the two proportions are approxamately normally distributed. 
#Comparison derived from: https://onlinecourses.science.psu.edu/stat414/node/268
from jaratoolbox import behavioranalysis
from jaratoolbox import loadbehavior
import numpy as np
from pylab import *
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportion_confint #Used to compute confidence interval for the error bars. 
from jaratoolbox import settings 
from scipy.stats import norm


#We want to be able to compare one subject accross multiple sessions, or two 
#subjects across the same session, or two subjects across two sessions.

subject1 = 'hm4d004'
session1 = '20140826a'

subject2 = 'hm4d005'
session2 = '20140826a'

fname1=loadbehavior.path_to_behavior_data(subject1,'nick','2afc',session1)
fname2=loadbehavior.path_to_behavior_data(subject2,'nick','2afc',session2)

bdata1=loadbehavior.BehaviorData(fname1)
bdata2=loadbehavior.BehaviorData(fname2)

def compare_props(x1, n1, x2, n2, hyp_0_difference=0):
    '''We could also consider using fisher's exact test, since it has no 
    assumptions of normality. The method here uses a z-test and assumes that
    the difference between the two proportions approximates a normal dist.
    '''
    phat1 = float(x1)/float(n1)
    phat2 = float(x2)/float(n2)
    phat = (float(x1) + float(x2))/(float(n1) + float(n2))
    zscore = ((phat1 - phat2) - hyp_0_difference)/np.sqrt(phat *(1-phat)*(1/float(n1) + 1/float(n2)))
    p_val = norm.sf(zscore)*2 #Two-sided test
    return p_val

def compute_psycurve(bdata):
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

    return nRightwardEachFreq, nTrialsEachFreq, fractionRightEachFreq, upperWhisker, lowerWhisker


nRightwardEachFreq1, nTrialsEachFreq1, fractionRightEachFreq1, upperWhisker1, lowerWhisker1 = compute_psycurve(bdata1)
nRightwardEachFreq2, nTrialsEachFreq2, fractionRightEachFreq2, upperWhisker2, lowerWhisker2 = compute_psycurve(bdata2)

mouse1data=zip(nRightwardEachFreq1, nTrialsEachFreq1)
mouse2data=zip(nRightwardEachFreq2, nTrialsEachFreq2)
zipdata = zip(mouse1data, mouse2data)

pvals = np.empty(len(nRightwardEachFreq1))
for indf, freqdata in enumerate(zipdata):
    x1 = freqdata[0][0]
    n1 = freqdata[0][1]
    x2 = freqdata[1][0]
    n2 = freqdata[1][1]
    freq_pval = compare_props(x1, n1, x2, n2)
    pvals[indf] = freq_pval


significant = pvals<0.05

x_inds = range(nFreq)
errorbar(x_inds, fractionRightEachFreq1, yerr = [lowerWhisker1, upperWhisker1], label="{0}, {1}".format(subject1, session1))
errorbar(x_inds, fractionRightEachFreq2, yerr = [lowerWhisker2, upperWhisker2], label="{0}, {1}".format(subject2, session2))

offset = 0.05
for ind in x_inds:
    if significant[ind]:
        text(ind, np.max([fractionRightEachFreq1[ind] + upperWhisker1[ind], fractionRightEachFreq2[ind] + upperWhisker2[ind]])+offset, "*", va = 'center', ha = 'center')

axhline(y=0.5, color = 'red')
legend(loc=2)
ylim([-0.1,1.1])
xlim([-0.5, nFreq-0.5])
ylabel('% Going to the Right')
ax1 = plt.gca()
tickLabels = possibleFreq.astype(float)/1000 #We have to pad with a zero at the beginning and end of the array of labels
tickLabels = np.insert(tickLabels, 0, 0)
tickLabels = np.append(tickLabels, 0)
ax1.set_xticklabels(tickLabels)
xlabel('Frequency (kHz)')
show()
