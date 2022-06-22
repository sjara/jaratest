
"""
Plot psychmetric curve for an animal trained with the fm_discrimination paradigm.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import extraplots
from jaratoolbox import extrastats
from scipy.optimize import curve_fit
from scipy.special import expit

subject = 'pamo026'
paradigm = '2afc'
sessions = ['20220308a','20220309a','20220310a']#,'20220304a','20211009a','20211006a']
#sessions = ['20220204a','20220203a','20220202a','20220201a']

removetable = str.maketrans('', '','a')
sessions_list = [s.translate(removetable) for s in sessions]
percentages_slope = []
spline_percentages_slope = []
y_final=[]
# Analyzing the data
N_reward = 0

for x in sessions: 
    print(x)
    behavFile = loadbehavior.path_to_behavior_data(subject, paradigm, x)
    bdata = loadbehavior.BehaviorData(behavFile)    
    right_choice_trials = np.where(bdata['choice']==2,0,bdata['choice']) # 2 shows only right sidetrials, type np array
    rightonly_slopes = right_choice_trials*bdata['targetFMslope'] 
    possible_slopes = np.unique(bdata['targetFMslope'])
    r_count_slope = [None] * len(possible_slopes)
    count_slope = [None] * len(possible_slopes)
    for i in range(len(possible_slopes)):
        r_count_slope[i] = np.count_nonzero(rightonly_slopes == possible_slopes[i])
        count_slope[i] = np.count_nonzero(bdata['targetFMslope'] == possible_slopes[i])
    percentages = [None] * len(r_count_slope)
    for i in range(len(percentages)):
        percentages[i] = round((r_count_slope[i]/count_slope[i])*100,2)
    percentages_slope.append(percentages)

'''
Psychometric function (allows defining asymptotes)
alpha: bias
beta : related to slope
lamb : lapse term (up). It should be a non-negative value, zero means curve goes to one.
gamma: lapse term (down). It should be a non-negative value, zero means curve goes to zero.
'''
for z in range (len(sessions)):
    print (z)
    xdata = possible_slopes
    ydata = np.array(percentages_slope[z])/100
#    p0 = [max(ydata), np.median(xdata),500,min(ydata)] # this is an mandatory initial guess
#    p0 = [ np.median(xdata),1,max(ydata),min(ydata)]
#    popt, pcov = curve_fit(psychfun, xdata, ydata,p0, method='lm')
# Example for fitting psychometric curve:
    paramInitial = [0, -0.5, 0, 0]
    paramBounds = [[-np.inf, -np.inf, 0, 0], [np.inf, np.inf, 0.5, 0.5]]
#    print(paramBounds)
    curveParams, pCov = curve_fit(extrastats.psychfun, xdata, ydata,
                                             p0=paramInitial, bounds=paramBounds)
    x = np.linspace(-1, 1, 1000)
    print(curveParams)
    y = extrastats.psychfun(x, *curveParams)
    y_final.append(y)

'''
    curveParams, pCov = curve_fit(extrastats.psychfun, xdata, ydata,
                                             p0=paramInitial, bounds=paramBounds)
'''    

print(percentages_slope)

#plotting 

plt.clf()
plt.subplot(1,3,1)
#plt.subplot(1,2,1)
plt.scatter(possible_slopes,percentages_slope[0])
plt.plot(x,100*y_final[0], label='fit')
plt.ylim(0, 100)
plt.xlabel("FM slopes")
plt.ylabel("Rightward trial percentage")
plt.title(sessions[0])
#2])
plt.subplot(1,3,2)
#plt.subplot(1,2,1)
plt.scatter(possible_slopes,percentages_slope[1])
plt.plot(x,100*y_final[1], label='fit')
plt.ylim(0, 100)
plt.xlabel("FM slopes")
plt.ylabel("Rightward trial percentage")
plt.title(sessions[1])
#2])
plt.subplot(1,3,3)
#plt.subplot(1,2,1)
plt.scatter(possible_slopes,percentages_slope[2])
plt.plot(x,100*y_final[2], label='fit')
plt.ylim(0, 100)
plt.xlabel("FM slopes")
plt.ylabel("Rightward trial percentage")
plt.title(sessions[2])
#2])



plt.show()


