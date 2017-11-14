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

summaryFilename = 'muscimol_num_trials_summary.npz'
summaryFullPath = os.path.join(outputDir,summaryFilename)

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
validMat = np.zeros((nAnimals, nSessions, nCond))
totalMat = np.zeros((nAnimals, nSessions, nCond))
subjects = [] #For saving

for indAnimal, animalName in enumerate(animalsToUse):
    animalSessionDict = animals[animalName]
    subjects.append(animalName)
    for indCond in [0, 1]:
        sessions = animalSessionDict[conditions[indCond]]
        for indSession, session in enumerate(sessions):
            bdata = behavioranalysis.load_many_sessions(animalName, [session])
            nValid = num_valid(bdata)
            validMat[indAnimal, indSession, indCond] = nValid

subjects = [] #For saving
for indAnimal, animalName in enumerate(animalsToUse):
    animalSessionDict = animals[animalName]
    subjects.append(animalName)
    for indCond in [0, 1]:
        sessions = animalSessionDict[conditions[indCond]]
        for indSession, session in enumerate(sessions):
            bdata = behavioranalysis.load_many_sessions(animalName, [session])
            nTotal = len(bdata['valid'])
            totalMat[indAnimal, indSession, indCond] = nTotal

np.savez(summaryFullPath,
         validMat = validMat,
         totalMat = totalMat,
         subjects = np.array(subjects),
         conditions = np.array(conditions),
         script = scriptFullPath
         )

print 'Saved results to {}'.format(summaryFullPath)
