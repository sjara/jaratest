import os
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
reload(settings)
import figparams
import numpy as np
from matplotlib import pyplot as plt
from jaratoolbox import extraplots
from muscimol_sessions import animals

FIGNAME = 'muscimol_inactivation'
outputDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
scriptFullPath = os.path.realpath(__file__)

summaryFilename = 'muscimol_response_time_summary.npz'
summaryFullPath = os.path.join(outputDir,summaryFilename)



# rt = bdata['timeCenterOut']-bdata['timeTarget']



animalsToUse = ['adap021', 'adap023', 'adap028', 'adap029', 'adap035']

nAnimals = len(animalsToUse)
nSessions = 4
nCond = 2
conditions = ['saline', 'muscimol'] #0 for saline, 1 for muscimol



#How to save it?
# rtMat = np.zeros((nAnimals, nCond, allRT))
subjects = [] #For saving

dataDict = {}

for indAnimal, animalName in enumerate(animalsToUse):
    animalSessionDict = animals[animalName]
    subjects.append(animalName)
    for indCond in [0, 1]:
        sessions = animalSessionDict[conditions[indCond]]
        for indSession, session in enumerate(sessions):
            bdata = behavioranalysis.load_many_sessions(animalName, [session])
            rtAll = bdata['timeCenterOut'] - bdata['timeTarget']
            rtValid = rtAll[bdata['valid']]

            dataDict.update({'{}all{}'.format(animalName, conditions[indCond]):rtAll,
                             '{}valid{}'.format(animalName, conditions[indCond]):rtValid})

np.savez(summaryFullPath,
         subjects = np.array(subjects),
         conditions = np.array(conditions),
         script = scriptFullPath,
         **dataDict
         )

print 'Saved results to {}'.format(summaryFullPath)
