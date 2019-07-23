import os
from jaratest.nick.behavior import behavioranalysis_vnick as ba
import statsmodels as sm
import pandas as pd
from matplotlib import pyplot as plt
from jaratoolbox import extraplots
import numpy as np

'''
Some references for the usage of statsmodels GLM to do binomial logistic regression:
https://stats.stackexchange.com/questions/92862/should-statsmodelss-glm-produce-the-same-results-as-rs-lm

https://www.statsmodels.org/dev/examples/notebooks/generated/glm_formula.html
'''

# animals = ['amod002', 'amod003']
animals = ['amod003']
sessions = ['20160412a', '20160413a', '20160414a', '20160415a', '20160416a',
               '20160417a', '20160418a', '20160419a', '20160420a', '20160421a']
muscimol = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]

allnCorr = []
allnVal = []
allfracCorr = []

sessionInd = []
animalInd = []
soundType = []
muscimolInjected = []

for indAnimal, animal in enumerate(animals):
    for indSession, session in enumerate(sessions):
        (bdataObjs, bdataSoundTypes) = ba.load_behavior_sessions_sound_type(animal, [session])
        for st in [0, 1]: #0 = mod, 1=chord
            bdata = bdataObjs[st]
            nCorr = sum(bdata['outcome']==bdata.labels['outcome']['correct'])
            nVal = sum(bdata['valid'])
            allfracCorr.append(nCorr.astype(float)/nVal)
            allnCorr.append(nCorr)
            allnVal.append(nVal)
            sessionInd.append(indSession)
            animalInd.append(indAnimal)
            soundType.append(st)
            muscimolInjected.append(muscimol[indSession])

nCorr = allnCorr
nIncorr = np.array(allnVal) - np.array(allnCorr)

data = pd.DataFrame({'nCorr':np.array(nCorr),
                     'nIncorr':np.array(nIncorr),
                     'soundType':np.array(soundType),
                     'muscimolInjected':np.array(muscimolInjected),
                     'sessionInd':np.array(sessionInd)})


res = sm.api.formula.glm(formula='nCorr + nIncorr ~ C(soundType)*C(muscimolInjected)', data=data, family=sm.api.families.Binomial()).fit()
print res.summary()

plt.clf()

## Calculate percent correct and binomial confidence interval for each group

# Muscimol AM group
nCorrMusAM = np.mean(data.query('muscimolInjected==1 and soundType==0')['nCorr'])
nIncorrMusAM = np.mean(data.query('muscimolInjected==1 and soundType==0')['nIncorr'])
percentCorrectMusAM = nCorrMusAM.astype(float) / (nCorrMusAM + nIncorrMusAM)
ciMusAM = np.array(sm.stats.proportion.proportion_confint(nCorrMusAM,
                                                          nCorrMusAM + nIncorrMusAM,
                                                          method = 'wilson'))
lowerMusAM = percentCorrectMusAM - ciMusAM[0]
upperMusAM = ciMusAM[1] - percentCorrectMusAM

# Saline AM group
nCorrSalAM = np.mean(data.query('muscimolInjected==0 and soundType==0')['nCorr'])
nIncorrSalAM = np.mean(data.query('muscimolInjected==0 and soundType==0')['nIncorr'])
percentCorrectSalAM = nCorrSalAM.astype(float) / (nCorrSalAM + nIncorrSalAM)
ciSalAM = np.array(sm.stats.proportion.proportion_confint(nCorrSalAM,
                                                          nCorrSalAM + nIncorrSalAM,
                                                          method = 'wilson'))
lowerSalAM = percentCorrectSalAM - ciSalAM[0]
upperSalAM = ciSalAM[1] - percentCorrectSalAM

# Muscimol Chords group
nCorrMusChords = np.mean(data.query('muscimolInjected==1 and soundType==1')['nCorr'])
nIncorrMusChords = np.mean(data.query('muscimolInjected==1 and soundType==1')['nIncorr'])
percentCorrectMusChords = nCorrMusChords.astype(float) / (nCorrMusChords + nIncorrMusChords)
ciMusChords = np.array(sm.stats.proportion.proportion_confint(nCorrMusChords,
                                                              nCorrMusChords + nIncorrMusChords,
                                                              method = 'wilson'))
lowerMusChords = percentCorrectMusChords - ciMusChords[0]
upperMusChords = ciMusChords[1] - percentCorrectMusChords

# Saline Chords group
nCorrSalChords = np.mean(data.query('muscimolInjected==0 and soundType==1')['nCorr'])
nIncorrSalChords = np.mean(data.query('muscimolInjected==0 and soundType==1')['nIncorr'])
percentCorrectSalChords = nCorrSalChords.astype(float) / (nCorrSalChords + nIncorrSalChords)
ciSalChords = np.array(sm.stats.proportion.proportion_confint(nCorrSalChords,
                                                              nCorrSalChords + nIncorrSalChords,
                                                              method = 'wilson'))
lowerSalChords = percentCorrectSalChords - ciSalChords[0]
upperSalChords = ciSalChords[1] - percentCorrectSalChords

# Lower and upper confidence intervals for the errorbar command
lowerAM = [lowerSalAM, lowerMusAM]
upperAM = [upperSalAM, upperMusAM]
lowerChords = [lowerSalChords, lowerMusChords]
upperChords = [upperSalChords, upperMusChords]

# Plot chords and AM as different lines (to compare slope)
plt.errorbar(x=[0,1], y=[percentCorrectSalAM, percentCorrectMusAM],
             yerr=[lowerAM, upperAM], ls='-', color='k', label='AM')
plt.errorbar(x=[0,1], y=[percentCorrectSalChords, percentCorrectMusChords],
             yerr=[lowerChords, upperChords], ls='--', color='k', label='Chords')
plt.legend()
plt.ylabel('Fraction correct')
plt.xlabel('Injection')
ax=plt.gca()
ax.set_xticks([0, 1])
ax.set_xticklabels(['Saline', 'Muscimol'])
ax.set_xlim([-0.25, 1.25])
ax.set_ylim([0.45, 1.05])
extraplots.boxoff(ax)
subject=animals[0]
plt.title(subject)

outputDir = '/home/nick/data/dissertation_amod'
figFn = 'figure_{}_interaction.png'.format(subject)
plt.savefig(os.path.join(outputDir, figFn))


plt.show()

