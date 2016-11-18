'''
Behavior analysis for go-signal mice.
'''

import numpy as np
from jaratoolbox import extraplots
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
import matplotlib.pyplot as plt
import sys
import matplotlib.pyplot as plt

#subject = sys.argv[1]
session = sys.argv[1]

'''
animalList = ['gosi010']

'''
animalList = ['gosi001','gosi002','gosi003','gosi004','gosi005',
              'gosi006','gosi007','gosi008','gosi009','gosi010',
              'gosi011','gosi012','gosi013','gosi014','gosi015']

nValidAll = []
fractionValidAll = []
fractionCorrectAll = []

    
plt.clf()
nSubjects = len(animalList)
#xvals = np.arange(1,len(animalList)+1)

for inds,subject in enumerate(animalList):
    behavFile = loadbehavior.path_to_behavior_data(subject,'2afc',session)
    bdata = loadbehavior.BehaviorData(behavFile)

    timeTarget = bdata['timeTarget']
    timeCenterOut = bdata['timeCenterOut']
    withdrawalTimeFromTargetOnset = timeCenterOut-timeTarget
    print('Median [{0}] = {1}'.format(animalList[inds],np.median(withdrawalTimeFromTargetOnset)))
    
    plt.subplot(nSubjects//2+1,2,inds+1)
    plt.hist(withdrawalTimeFromTargetOnset,bins=60,range=[-0.1,0.8],fc='g',ec='g')
    plt.ylabel('{0}'.format(animalList[inds]))
    #plt.ylabel('N trials [{0}]'.format(animalList[inds]))
    plt.xlim([-0.1,0.8])
    #plt.plot(withdrawalTimeFromTargetOnset,drawstyle='steps')

    if inds==0:
        plt.title('Withdrawal time from sound onset')
    plt.draw()
    plt.show()
    
plt.xlabel('Time from sound onset')

'''
plt.subplot(nSubjects//2+1,2,)
plt.bar(xvals, nValidAll, align='center', color='0.75')
plt.ylabel('N valid')
plt.xlim([0,nSubjects+1])
plt.title('Go-signal mice - {0}'.format(session), fontweight='bold')

plt.subplot(3,1,2)
plt.bar(xvals, 100*np.array(fractionValidAll), align='center', color='g')
plt.ylabel('% valid')
plt.ylim([0,100])
plt.xlim([0,nSubjects+1])

plt.subplot(3,1,3)
plt.bar(xvals, 100*np.array(fractionCorrectAll), align='center', color='b')
plt.ylabel('% correct')
plt.ylim([0,100])
plt.xlim([0,nSubjects+1])
'''

plt.show()
