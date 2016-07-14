
from jaratoolbox import behavioranalysis

# def load_behavior_sessions_sound_type(animal, sessions):

#     '''
#     Load many sessions (or only one) and then divide up into several bdata objects based on the type of
#     sound that was presented.

#     Args
#     animal (str): The name of the animal
#     sessions (list of strings): Sessions to load

#     Returns
#     dataObjs (list of jaratoolbox.behavioranalysis.LoadBehaviorData objects): behavior data objects for each sound type
#     dataSoundTypes (list of strings): The sound type that corresponds to each of the data objects

#     '''

#     bdata = behavioranalysis.load_many_sessions(animal, sessions)
#     soundTypes = [bdata.labels['soundType'][x] for x in np.unique(bdata['soundType'])]

#     dataObjs = []
#     dataSoundTypes = []

#     for thisType in soundTypes:
#         bdataThisType = behavioranalysis.load_many_sessions(animal, sessions)

#         #The inds where this kind of sound was presented
#         indsThisType = bdataThisType['soundType']==bdataThisType.labels['soundType'][thisType]

#         #All other inds
#         notIndsThisType = np.logical_not(indsThisType)

#         #Remove all trials where this type was not presented
#         bdataThisType.remove_trials(notIndsThisType)

#         #Save out the bdata object and the sound type
#         dataObjs.append(bdataThisType)
#         dataSoundTypes.append(thisType)

#     return (dataObjs, dataSoundTypes)


from jaratoolbox.test.nick import behavioranalysis_vnick as behavioranalysis




from jaratoolbox import extrastats
from jaratoolbox import extraplots


bdata = amod002salineData[0]

# rightTrials = bdata['choice']==bdata.labels['choice']['right']
# freqEachTrial = bdata['targetFrequency']
# valid = bdata['valid']
# (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue) = behavioranalysis.calculate_psychometric(rightTrials, freqEachTrial, valid)
# estimate = extrastats.psychometric_fit(possibleValues, nTrialsEachValue, nHitsEachValue)

# yvals = nHitsEachValue.astype(float)/nTrialsEachValue
# xvals = possibleValues
# xRange = xvals[-1]-xvals[0]
# fitxval = np.linspace(xvals[0]-0.1*xRange,xvals[-1]+0.1*xRange,40)
# fityval = extrastats.psychfun(fitxval,*estimate)
# hfit = plot(fitxval,100*fityval,'-',linewidth=2)


def plot_fitted_psycurve(bdata, color='k', linestyle=None):
    rightTrials = bdata['choice']==bdata.labels['choice']['right']
    freqEachTrial = bdata['targetFrequency']
    valid = bdata['valid']
    (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue) = behavioranalysis.calculate_psychometric(rightTrials, freqEachTrial, valid)

    pline, pcaps, pbars, pdots = extraplots.plot_psychometric(possibleValues, fractionHitsEachValue, ciHitsEachValue)
    setp(pline, color='w')
    setp(pcaps, color=color)
    setp(pbars, color=color)
    setp(pdots, markerfacecolor=color)

    estimate = extrastats.psychometric_fit(possibleValues, nTrialsEachValue, nHitsEachValue)

    yvals = nHitsEachValue.astype(float)/nTrialsEachValue
    xvals = possibleValues
    xRange = xvals[-1]-xvals[0]
    fitxval = np.linspace(xvals[0]-0.1*xRange,xvals[-1]+0.1*xRange,40)
    fityval = extrastats.psychfun(fitxval,*estimate)
    hfit = plot(fitxval,100*fityval,'-',linewidth=2, color=color)

    return (estimate, (pline, pcaps, pbars, pdots, hfit))

def plot_muscimol_fitted_curves(salineData, muscimolData):

    salineEstimate, plotObjs = plot_fitted_psycurve(salineData, color='k')
    hold(1)
    muscimolEstimate, plotObjs = plot_fitted_psycurve(muscimolData, color='r')

    return (salineEstimate, muscimolEstimate)

muscimolSessions = ['20160413a', '20160415a', '20160417a', '20160419a', '20160421a']
salineSessions = ['20160412a', '20160414a', '20160416a', '20160418a', '20160420a']


animal = 'amod002'

amod002salineData, amod002salineDataSounds = behavioranalysis.load_behavior_sessions_sound_type(animal, salineSessions)
amod002muscimolData, amod002muscimolDataSounds = behavioranalysis.load_behavior_sessions_sound_type(animal, muscimolSessions)



clf()
subplot(121)
salineEstimate,muscimolEstimate = plot_muscimol_fitted_curves(amod002salineData[0], amod002muscimolData[0])

subplot(122)
salineEstimate,muscimolEstimate = plot_muscimol_fitted_curves(amod002salineData[1], amod002muscimolData[1])

figure()
st0SalineBeta = []
st1SalineBeta = []
for saline in salineSessions:
    thisSalineData, thisSalineSounds = behavioranalysis.load_behavior_sessions_sound_type(animal, [saline])
    estimate0, plotObjs = plot_fitted_psycurve(thisSalineData[0])
    st0SalineBeta.append(estimate0[1])
    estimate1, plotObjs = plot_fitted_psycurve(thisSalineData[1])
    st1SalineBeta.append(estimate1[1])

st0MuscimolBeta = []
st1MuscimolBeta = []
for muscimol in muscimolSessions:
    thisMuscimolData, thisMuscimolSounds = behavioranalysis.load_behavior_sessions_sound_type(animal, [muscimol])
    estimate0, plotObjs = plot_fitted_psycurve(thisMuscimolData[0])
    st0MuscimolBeta.append(estimate0[1])
    estimate1, plotObjs = plot_fitted_psycurve(thisMuscimolData[1])
    st1MuscimolBeta.append(estimate1[1])

