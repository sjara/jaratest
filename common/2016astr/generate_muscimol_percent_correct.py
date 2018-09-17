import numpy as np
import copy
from matplotlib import pyplot as plt
from scipy import stats
from jaratoolbox import loadbehavior
from jaratoolbox import extraplots
import muscimol_sessions

subjects = ['adap021', 'adap023', 'adap028', 'adap029', 'adap035']

#Init array to hold percent correct for 4 saline sessions for each animal
percCorrect = np.empty((len(subjects), 4))

for indSubject, subject in enumerate(subjects):
    datesDict = muscimol_sessions.animals[subject]
    alldates = []
    salinedates = datesDict['saline']
    muscimoldates = datesDict['muscimol']
    sessions = salinedates
    for indSession, session in enumerate(sessions):
        #Load behavior data for the sessioln
        bfile = loadbehavior.path_to_behavior_data(subject, '2afc', session)
        bdata = loadbehavior.BehaviorData(bfile)

        #Compute percent correct for valid trials
        valid = bdata['valid']
        correct = bdata['outcome'] == bdata.labels['outcome']['correct']
        validCorrect = (valid & correct)
        numValid = sum(valid)
        numCorrect = sum(validCorrect)
        percCorrect[indSubject, indSession] = (numCorrect/float(numValid))*100

#Related-samples t-test between first and last saline day
firstSaline = percCorrect[:,0]
lastSaline = percCorrect[:,-1]
zVal, pVal = stats.ttest_rel(firstSaline, lastSaline)
print "Related sample t-test between percent correct on first and last day, p = {}".format(pVal)

#Plot percent correct on first and last saline day
# plt.clf()
# plt.plot(np.zeros(len(subjects)), firstSaline, 'o', mec='k', mfc='None')
# plt.hold(1)
# plt.plot(np.ones(len(subjects)), lastSaline, 'o', mec='k', mfc='None')
# plt.xlim([-0.5, 1.5])
# plt.ylabel('% correct')
# plt.ylim([50, 100])
# ax = plt.gca()
# ax.set_xticks([0,1])
# ax.set_xticklabels(['First saline session', 'Last saline session'])
# extraplots.new_significance_stars([0, 1], 95, 2.5, starMarker='n.s.', fontSize=12, gapFactor=0.25)
# extraplots.boxoff(ax)
# plt.show()
# plt.savefig('/tmp/saline_percent_correct.png')

plt.clf()
for indSubject, subject in enumerate(subjects):
    plt.hold(1)
    plt.plot(percCorrect[indSubject, :], '-o', color='0.5', mfc='None')
meanPercCorrect = np.mean(percCorrect, axis=0)
plt.xlim([-0.5, 3.5])
plt.ylabel('% correct')
plt.ylim([50, 100])
ax = plt.gca()
ax.set_xticks(range(4))
ax.set_xticklabels([1, 2, 3, 4])
ax.set_xlabel('Saline session')
# ax.set_xticklabels(['First saline session', 'Last saline session'])
# extraplots.new_significance_stars([0, 1], 95, 2.5, starMarker='n.s.', fontSize=12, gapFactor=0.25)
slope, intercept, rVal, pVal, err = stats.linregress(range(len(meanPercCorrect)), meanPercCorrect)
xvals = np.array([0, 1, 2, 3])
yPred = xvals*slope + intercept
plt.plot(xvals, yPred, '-', color='k', lw=3)
print "linear regression of saline day against % correct: slope: {}, intercept: {}, rVal: {}, pVal: {}, err: {}".format(slope, intercept, rVal, pVal, err)
extraplots.boxoff(ax)
plt.show()
# plt.savefig('/tmp/saline_percent_correct.png')
