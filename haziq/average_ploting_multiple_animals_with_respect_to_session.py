
"""
Plot psychmetric curve for an animal trained with the fm_discrimination paradigm.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import extraplots

#subject = ['pamo009', 'pamo011', 'pamo012', 'pamo013', 'pamo016', 'pamo019', 'pamo022', 'pamo026']
subject = ['pamo010', 'pamo014', 'pamo015', 'pamo017', 'pamo018', 'pamo021', 'pamo023', 'pamo025']
paradigm = '2afc'
#session = '20211201a'
sessions = ['20220201a','20220202a','20220203a','20220204a',
            '20220205a','20220206a','20220207a','20220208a',
            '20220209a','20220210a','20220211a','20220212a',
            '20220213a','20220214a']
avg_performance = []
multiple_avg_perf= []

print ("ploting average performances of " + str(subject) +" animals")
n=0
for y in subject:
    #print (y)
    avg_performance = []
    for x in sessions: 
        behavFile = loadbehavior.path_to_behavior_data(y, paradigm, x)
        bdata = loadbehavior.BehaviorData(behavFile)
        correct_trials_count = np.count_nonzero(bdata['outcome'] == bdata.labels['outcome']['correct']) #no of correct trials type int
        valid_trials_count = np.count_nonzero(bdata['valid'] == True)  #no of valid trials type int    
        average_performance = (correct_trials_count/valid_trials_count)*100 # type float
        #print("The avarage performance for "+ str (y) + " on"+ str(x) + "is " + str("{:.2f}".format(average_performance)) +" %.")
        avg_performance.append(float("{:.2f}".format(average_performance))) # type list
    multiple_avg_perf.append(avg_performance) # list with in list
    n +=1

x = np.arange(1, (len(sessions)+1), 1) # numpy array
plt.xlabel("No. of days at stage 3")
plt.ylabel("Percentage")
plt.title("Average performance")
#xTicks = np.arange(0, 9, 1)
for i in range(len(multiple_avg_perf)): 
    plt.plot(sessions,multiple_avg_perf[i], label = subject[i])
plt.xticks(sessions, x)
plt.ylim(0, 100)
plt.legend(loc="upper left")
plt.show()

#'antibiasMode':
