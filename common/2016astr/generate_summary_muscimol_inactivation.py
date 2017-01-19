'''
This will generate the data required for the summary plot for this figure, which will be
a paired comparison of average percent correct in saline and muscimol trials


OVERALL METHOD

Should we calculate the percent correct and the cis by loading all the sessions and using
the binomial confidence interval, or by calculating the percent correct for each session
and using the sd as the error bars?

I am currently using the first method, loading all the sessions together

'''
import os
import figparams
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
reload(settings)
import figparams
import numpy as np
from muscimol_sessions import animals

FIGNAME = 'muscimol_inactivation'
outputDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
scriptFullPath = os.path.realpath(__file__)

summaryFilename = 'muscimol_frac_correct_summary.npz'
summaryFullPath = os.path.join(outputDir,summaryFilename)

def frac_correct(bdata):
    '''
    Calculate the fraction of correct trials overall for a bdata object.

    Args:
        bdata (jaratoolbox.loadbehavior.BehaviorData dict): the behavior data to use
    Returns:
        nCorrect (int): Number of correct trials
        nValid (int): Number of valid trials
    '''
    correct = bdata['outcome']==bdata.labels['outcome']['correct']
    nCorrect = sum(correct)
    valid = bdata['valid']
    nValid = sum(valid)
    return nCorrect/float(nValid)


# animalNames = animals.keys()
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
            fracCorrect = frac_correct(bdata)
            dataMat[indAnimal, indSession, indCond] = fracCorrect

np.savez(summaryFullPath,
         data = dataMat,
         subjects = np.array(subjects),
         conditions = np.array(conditions),
         script = scriptFullPath
         )

print 'Saved results to {}'.format(summaryFullPath)

'''
animalNames = []
nCorrectSalEachMouse = []
nValidSalEachMouse = []
nCorrectMusEachMouse = []
nValidMusEachMouse = []
nSalineSessions = []
nMuscimolSessions = []
'''
