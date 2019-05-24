import numpy as np
import pypsignifit
from jaratoolbox import extrastats
from jaratoolbox import extraplots
from matplotlib import pyplot as plt
# from jaratest.nick import behavioranalysis_vnick as behavioranalysis
from jaratest.nick.behavior import behavioranalysis_vnick as behavioranalysis

### For plotting a single session
# muscimolSessions = ['20160413a', '20160415a', '20160417a', '20160419a', '20160421a']
# salineSessions = ['20160412a', '20160414a', '20160416a', '20160418a', '20160420a']
# animal = 'amod002'

# #Load the data objects for the muscimol and saline sessions
# muscimolDataObjs, muscimolSoundTypes = behavioranalysis.load_behavior_sessions_sound_type(animal, muscimolSessions)
# salineDataObjs, salineSoundTypes = behavioranalysis.load_behavior_sessions_sound_type(animal, salineSessions)

# #Testing with a single bdata object
# # hold(1)
# bdata = salineDataObjs[0]
# bdata = muscimolDataObjs[0]

# plt.clf()

# #Calculate hit trials, freq each trial, valid - then calc psychometric
# rightTrials = bdata['choice']==bdata.labels['choice']['right']
# freqEachTrial = bdata['targetFrequency']
# valid = bdata['valid']

# (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue) = behavioranalysis.calculate_psychometric(rightTrials, freqEachTrial, valid)

# extraplots.plot_psychometric(possibleValues, fractionHitsEachValue, ciHitsEachValue)

# #calculating the estimate without constraints
# # estimate = extrastats.psychometric_fit(possibleValues, nTrialsEachValue, nHitsEachValue)

# #Calculating with constraints
# constraints = ( 'Uniform(8, 32)','Uniform(0,20)' ,'Uniform(0,1)', 'Uniform(0,1)')
# estimate = extrastats.psychometric_fit(possibleValues, nTrialsEachValue, nHitsEachValue, constraints)

# #The x values over which to evaluate the fitted function
# xRange = possibleValues[-1]-possibleValues[1]
# fitxval = np.linspace(possibleValues[0]-0.1*xRange,possibleValues[-1]+0.1*xRange,40)

# #The fitted points
# fityvals = extrastats.psychfun(fitxval, estimate[0], estimate[1], estimate[2], estimate[3])

# # hold(1)
# plt.plot(fitxval, fityvals*100)

# musAmpEstimates = np.zeros([len(muscimolSessions), 4])
# musChordEstimates = np.zeros([len(muscimolSessions), 4])
# salineAmpEstimates = np.zeros([len(salineSessions), 4])
# salineChordEstimates = np.zeros([len(salineSessions), 4])

labelFontSize = 5

#############################################
# These are the days for amod002 and amod003#
# animal = 'amod003'
# muscimolSessions = ['20160413a', '20160415a', '20160417a', '20160419a', '20160421a']
# salineSessions = ['20160412a', '20160414a', '20160416a', '20160418a', '20160420a']

# allSessions = ['20160412a', '20160413a', '20160414a', '20160415a', '20160416a',
#                '20160417a', '20160418a', '20160419a', '20160420a', '20160421a']
# sessionType = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
#############################################

#############################################
# These are the days for amod004
animal = 'amod004'
# muscimolSessions = ['20160427a', '20160429a', '20160501a', '20160503a', '20160505a', '20160507a', '20160509a']
# salineSessions = ['20160426a', '20160428a', '20160430a', '20160502a', '20160504a', '20160506a', '20160508a']

# allSessions = ['20160426a', '20160427a', '20160428a', '20160429a', '20160430a', '20160501a', '20160502a',
#                '20160503a', '20160504a', '20160505a', '20160506a', '20160507a', '20160508a', '20160509a']
# sessionType = [0,1,0,1,0,1,0,1,0,1,0,1,0,1]

#Just plot the first 5
allSessions = ['20160426a', '20160427a', '20160428a', '20160429a', '20160430a', '20160501a', '20160502a',
               '20160503a', '20160504a', '20160505a']
sessionType = [0,1,0,1,0,1,0,1,0,1]
#############################################



ampEstimates = np.zeros([len(allSessions), 4])
chordEstimates = np.zeros([len(allSessions), 4])
# 0 for saline, 1 for muscimol
sessionColors = ['k', 'r']

plt.close('all')
plt.figure()
for indSession, session in enumerate(allSessions):
    theseDataObjs, theseSoundTypes = behavioranalysis.load_behavior_sessions_sound_type(animal, [session])
    thisColor = sessionColors[sessionType[indSession]]

    ax = plt.subplot2grid((2, len(allSessions)), (0, indSession))
    ampEstimates[indSession, :] = behavioranalysis.plot_psycurve_fit_and_data(theseDataObjs[0], thisColor) #The amp_mod session
    ax.tick_params(axis='both', which='major', labelsize=labelFontSize)
    ax.tick_params(axis='both', which='minor', labelsize=labelFontSize)
    plt.title('{}'.format(session))
    behavioranalysis.nice_psycurve_settings(ax, fontsize=10, lineweight=2, fitlineinds=[0])
    ax.set_xlabel('AM rate (Hz)')
    if indSession>0:
        ax.set_ylabel('')
    else:
        ax.set_ylabel('AM\nFraction rightward trials')

    plt.subplots_adjust(hspace=0.4, wspace=0.4)

    ax = plt.subplot2grid((2, len(allSessions)), (1, indSession))
    chordEstimates[indSession, :] = behavioranalysis.plot_psycurve_fit_and_data(theseDataObjs[1], thisColor)
    ax.tick_params(axis='both', which='major', labelsize=labelFontSize)
    ax.tick_params(axis='both', which='minor', labelsize=labelFontSize)
    # plt.title('{}'.format([key for key, value in theseSoundTypes.iteritems()][1]))
    behavioranalysis.nice_psycurve_settings(ax, fontsize=10, lineweight=2, fitlineinds=[0])
    if indSession>0:
        ax.set_ylabel('')
    else:
        ax.set_ylabel('Chords\nFraction rightward trials')

figSize = [30, 6]

# figtext(0.075, 0.7, 'Fraction of trials going to the right', rotation='vertical')
# figtext(0.4, 0.05, 'Log2(frequency) - octaves')
plt.suptitle(animal)
plt.gcf().set_facecolor('w')
outputDir = '/home/nick/data/dissertation_amod'
extraplots.save_figure('{}_muscimol_inactivation_daily'.format(animal), 'png', figSize, outputDir=outputDir)

plt.show()


