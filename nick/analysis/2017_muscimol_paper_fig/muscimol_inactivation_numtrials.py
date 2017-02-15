import os
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
reload(settings)
import numpy as np
from matplotlib import pyplot as plt
from jaratoolbox import extraplots

import copy

adap021 = {
    #Muscimol 0.125mg/ml
    'muscimol0125' : ['20160803a', '20160808a', '20160810a', '20160812a'],
    #Saline for muscimol 0.125mg/ml
    'saline_muscimol0125' : ['20160802a', '20160804a', '20160809a', '20160811a'],
    #Muscimol 0.25 mg/ml
    'muscimol0250' : ['20160816a', '20160818a', '20160822a', '20160824a'],
    #Saline for muscimol 0.250mg/ml
    'saline_muscimol0250' : ['20160815a', '20160817a', '20160819a', '20160823a']
}
#alias "muscimol" to the 0.25mg/ml sessions
adap021.update({'muscimol':adap021['muscimol0250']})
#alias "saline" to the sessions collected when we were doing
#0.25mg/ml muscimol sessions
adap021.update({'saline':adap021['saline_muscimol0250']})

adap028 = {
    #Saline for 0.125mg/ml
    'saline_muscimol0125' : ['20160728a', '20160726a', '20160723a'],
    #Muscimol 0.125 mg/ml
    'muscimol0125' : ['20160729a', '20160727a', '20160725a', '20160721a'],
    #Muscimol 0.0625 mg/ml
    'muscimol00625' : ['20160722a'],
    #Saline for muscimol 0.25mg/ml
    'saline' : ['20160720a', '20160718a', '20160715a', '20160713a'],
    #Muscimol 0.250mg/ml
    'muscimol0250' : ['20160719a', '20160716a', '20160714a', '20160712a'],
}
#alias "muscimol" to the 0.25mg/ml sessions
adap028.update({'muscimol':adap028['muscimol0250']})

#Adap028 and adap029 were run together
adap029 = copy.deepcopy(adap028)

adap023 = {'muscimol': ['20160429a', '20160501a', '20160503a', '20160505a'],
           'saline': ['20160428a', '20160430a', '20160502a', '20160504b']}

adap032 = {'muscimol0250': ['20161130a', '20161202a', '20161204a', '20161206a'],
           'saline': ['20161129a', '20161201a', '20161203a', '20161205a']}
#alias "muscimol" to the 0.25mg/ml sessions
adap032.update({'muscimol':adap032['muscimol0250']})

adap033 = {'muscimol0250': ['20161130a', '20161202a', '20161204a', '20161206a'],
           'saline': ['20161129a', '20161201a', '20161203a', '20161205a'],
           'fluomus': ['20161212a'],
           'fluosal': ['20161209a']}
#alias "muscimol" to the 0.25mg/ml sessions
adap033.update({'muscimol':adap033['muscimol0250']})

adap035 = {'muscimol0250': ['20161130a', '20161202a', '20161204a', '20161206a'],
           'saline': ['20161129a', '20161201a', '20161203a', '20161205a'],
           'fluomus': ['20161208a'],
           'fluosal': ['20161205a']}
#alias "muscimol" to the 0.25mg/ml sessions
adap035.update({'muscimol':adap035['muscimol0250']})

animals = {'adap021':adap021,
           'adap028':adap028,
           'adap029':adap029,
           'adap023':adap023,
           'adap032':adap032,
           'adap033':adap033,
           'adap035':adap035}



def num_valid(bdata):
    '''
    Calculate the fraction of correct trials overall for a bdata object.

    Args:
        bdata (jaratoolbox.loadbehavior.BehaviorData dict): the behavior data to use
    Returns:
        nValid (int): Number of valid trials
    '''
    valid = bdata['valid']
    nValid = sum(valid)
    return nValid


animalsToUse = ['adap021', 'adap023', 'adap028', 'adap029', 'adap035']

nAnimals = len(animalsToUse)
nSessions = 4
nCond = 2
conditions = ['saline', 'muscimol'] #0 for saline, 1 for muscimol
dataMat = np.zeros((nAnimals, nSessions, nCond))

subjects = [] #For saving

for indAnimal, animalName in enumerate(animalsToUse):
    animalSessionDict = animals[animalName]
    subjects.append(animalName)
    for indCond in [0, 1]:
        sessions = animalSessionDict[conditions[indCond]]
        for indSession, session in enumerate(sessions):
            bdata = behavioranalysis.load_many_sessions(animalName, [session])
            nValid = num_valid(bdata)
            dataMat[indAnimal, indSession, indCond] = nValid


ax2 = plt.subplot(111)

#dataMat(subject, session, condition)
ind = np.arange(len(subjects))
width = 0.35
condColors = ['k', 'r']

shiftAmt = width*0.05
# shiftAmt = 0
fontSizeLabels = 12
fontSizeTicks = 10

#FIXME: Hardcoded number of points per animal here
pointShift = np.array([-shiftAmt, shiftAmt, -shiftAmt, shiftAmt])

for indSubject, subject in enumerate(subjects):
    for indCond, condition in enumerate(conditions):
        sessionsThisCondThisSubject = dataMat[indSubject, :, indCond]
        ax2.plot(np.zeros(len(sessionsThisCondThisSubject)) + (indSubject + 0.5*width + indCond*width) + pointShift,
                sessionsThisCondThisSubject, marker='o', linestyle='none', mec=condColors[indCond], mfc='none')
        ax2.hold(1)

rects1 = ax2.bar(ind, dataMat[:, :, 0].mean(1)-0.5, width, bottom=0.5, edgecolor='k', facecolor='w')
rects2 = ax2.bar(ind+width+0.015, dataMat[:, :, 1].mean(1)-0.5, width, bottom=0.5, edgecolor='r', facecolor='w')

ax2.set_xticks(ind + width)
ax2.set_xticklabels(np.arange(6)+1, fontsize=fontSizeLabels)
ax2.set_xlabel('Mouse', fontsize=fontSizeLabels)
ax2.axhline(y=0.5, color='0.5', linestyle='-')
# ax2.set_ylim([0.45, 1])
ax2.set_xlim([ind[0]-0.5*width, ind[-1]+2.5*width ])
ax2.set_ylabel('Number of Trials', fontsize=fontSizeLabels)
# ax2.set_yticks([0.5, 1])

extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
extraplots.boxoff(ax2)
# ax2.annotate('C', xy=(labelPosX[0],labelPosY[0]), xycoords='axes fraction', fontsize=fontSizePanel, fontweight='bold')

plt.show()


for indSubject in range(5):
    subDataSal = dataMat[indSubject, :, 0]
    subDataMus = dataMat[indSubject, :, 1]

    print indSubject
    print stats.ranksums(subDataSal, subDataMus)
