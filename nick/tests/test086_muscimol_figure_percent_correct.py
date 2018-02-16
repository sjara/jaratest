import numpy as np
import copy
from matplotlib import pyplot as plt
from scipy import stats
from jaratoolbox import loadbehavior
from jaratoolbox import extraplots

########################################################################################3
####### Copied muscimol_sessions.py from jaratest.common.2016astr becuase I can't import it
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

############ End copied part ###########################################################
########################################################################################

############ New stuff below here ###############


subjects = ['adap021', 'adap023', 'adap028', 'adap029', 'adap035']

#Init array to hold percent correct for 4 saline sessions for each animal
percCorrect = np.empty((len(subjects), 4))

for indSubject, subject in enumerate(subjects):
    datesDict = animals[subject]
    alldates = []
    salinedates = datesDict['saline']
    muscimoldates = datesDict['muscimol']
    sessions = salinedates
    for indSession, session in enumerate(sessions):
        #Load behavior data for the session
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

