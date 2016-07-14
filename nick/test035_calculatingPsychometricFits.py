import pypsignifit
from jaratoolbox import extrastats
from jaratoolbox import extraplots
from jaratoolbox.test.nick import behavioranalysis_vnick as behavioranalysis

muscimolSessions = ['20160413a', '20160415a', '20160417a', '20160519a', '20160921a']
salineSessions = ['20160412a', '20160414a', '20160416a', '20160518a', '20160520a']
animal = 'amod002'

#Load the data objects for the muscimol and saline sessions
muscimolDataObjs, muscimolSoundTypes = behavioranalysis.load_behavior_sessions_sound_type(animal, muscimolSessions)
salineDataObjs, salineSoundTypes = behavioranalysis.load_behavior_sessions_sound_type(animal, salineSessions)

#Testing with a single bdata object
hold(1)
bdata = salineDataObjs[0]
bdata = muscimolDataObjs[0]

#Calculate hit trials, freq each trial, valid - then calc psychometric
rightTrials = bdata['choice']==bdata.labels['choice']['right']
freqEachTrial = bdata['targetFrequency']
valid = bdata['valid']

(possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue) = behavioranalysis.calculate_psychometric(rightTrials, freqEachTrial, valid)

extraplots.plot_psychometric(possibleValues, fractionHitsEachValue, ciHitsEachValue)

#calculating the estimate without constraints
estimate = extrastats.psychometric_fit(possibleValues, nTrialsEachValue, nHitsEachValue)

#Calculating with constraints
constraints = ( 'Uniform(8, 32)','Uniform(0,20)' ,'Uniform(0,1)', 'Uniform(0,1)')
estimate = extrastats.psychometric_fit(possibleValues, nTrialsEachValue, nHitsEachValue, constraints)

#The x values over which to evaluate the fitted function
xRange = possibleValues[-1]-possibleValues[1]
fitxval = np.linspace(possibleValues[0]-0.1*xRange,possibleValues[-1]+0.1*xRange,40)

#The fitted points
fityvals = extrastats.psychfun(fitxval, estimate[0], estimate[1], estimate[2], estimate[3])

hold(1)
plot(fitxval, fityvals*100)


muscimolSessions = ['20160413a', '20160415a', '20160417a']
salineSessions = ['20160412a', '20160414a', '20160416a']

musAmpEstimates = np.zeros([len(muscimolSessions), 4])
musChordEstimates = np.zeros([len(muscimolSessions), 4])
salineAmpEstimates = np.zeros([len(salineSessions), 4])
salineChordEstimates = np.zeros([len(salineSessions), 4])


def plot_psycurve_fit_and_data(bdata, plotFits=True):
    rightTrials = bdata['choice']==bdata.labels['choice']['right']
    freqEachTrial = bdata['targetFrequency']
    valid = bdata['valid']

    (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue) = behavioranalysis.calculate_psychometric(rightTrials, freqEachTrial, valid)

    #Calculate the lower and upper freq in the bdata to set the correct constraints
    # possibleFreq = np.unique(freqEachTrial)
    possibleFreq = np.log2(np.unique(freqEachTrial))
    maxFreq = max(possibleFreq)
    minFreq = min(possibleFreq)


    #Calculating with constraints
    # constraints = ( 'Uniform({}, {})'.format(minFreq, maxFreq),'Uniform(0,20)' ,'Uniform(0,1)', 'Uniform(0,1)')
    constraints = ( 'Uniform({}, {})'.format(minFreq, maxFreq), 'Uniform(0,10)' ,'Uniform(0,0.2)', 'Uniform(0,0.2)')
    estimate = extrastats.psychometric_fit(possibleValues, nTrialsEachValue, nHitsEachValue, constraints)

    if plotFits:
        xRange = possibleFreq[-1]-possibleFreq[1]
        fitxval = np.linspace(possibleFreq[0]-0.1*xRange,possibleFreq[-1]+0.1*xRange,40)

        #The fitted points
        fityvals = extrastats.psychfun(fitxval, estimate[0], estimate[1], estimate[2], estimate[3])

        plot(fitxval, fityvals)
        # hold(1)
        # extraplots.plot_psychometric(possibleFreq, fractionHitsEachValue, ciHitsEachValue)
        plot(np.log2(possibleFreq), fractionHitsEachValue, 'bo')

    return estimate





def plot_psycurve_fit_and_data_nohigh(bdata, plotFits=True):

    '''
    This version actually works. Calculates things in log2(freq) space.
    '''

    rightTrials = bdata['choice']==bdata.labels['choice']['right']
    freqEachTrial = bdata['targetFrequency']
    valid = bdata['valid']

    (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue) = behavioranalysis.calculate_psychometric(rightTrials, freqEachTrial, valid)

    plot(np.log2(possibleValues), fractionHitsEachValue, 'bo')
    hold(1)

    possibleFreq = np.log2(np.unique(freqEachTrial))
    lowerFreqConstraint = possibleFreq[1]
    upperFreqConstraint = possibleFreq[-2]
    maxFreq = max(possibleFreq)
    minFreq = min(possibleFreq)

    constraints = ( 'Uniform({}, {})'.format(lowerFreqConstraint, upperFreqConstraint), 'Uniform(0,5)' ,'Uniform(0,1)', 'Uniform(0,1)')
    estimate = extrastats.psychometric_fit(possibleFreq[:-1], nTrialsEachValue[:-1], nHitsEachValue[:-1], constraints)

    xRange = possibleFreq[-1]-possibleFreq[1]
    fitxval = np.linspace(possibleFreq[0]-0.1*xRange,possibleFreq[-1]+0.1*xRange,40)

    fityvals = extrastats.psychfun(fitxval, *estimate)

    plot(fitxval, fityvals)
    ylim([0, 1])

    return estimate




animal = 'amod003'
animal = 'amod002'

muscimolSessions = ['20160413a','20160415a','20160417a', '20160419a', '20160421a']
salineSessions = ['20160412a','20160414a','20160416a', '20160418a', '20160420a']


animal = 'amod004'
muscimolSessions = ['20160427a', '20160429a', '20160501a', '20160503a', '20160505a', '20160507a', '20160509a']
salineSessions = ['20160426a', '20160428a', '20160430a', '20160502a', '20160504a', '20160506a', '20160508a']


musAmpEstimates = np.zeros([len(muscimolSessions), 4])
musChordEstimates = np.zeros([len(muscimolSessions), 4])
salineAmpEstimates = np.zeros([len(salineSessions), 4])
salineChordEstimates = np.zeros([len(salineSessions), 4])

labelFontSize = 9

figure()
for indSession, session in enumerate(muscimolSessions):
    muscimolDataObjs, muscimolSoundTypes = behavioranalysis.load_behavior_sessions_sound_type(animal, [session])

    ax = subplot2grid((2, len(muscimolSessions)), (0, indSession))
    musAmpEstimates[indSession, :] = behavioranalysis.plot_psycurve_fit_and_data(muscimolDataObjs[0], 'r') #The amp_mod session
    ax.tick_params(axis='both', which='major', labelsize=labelFontSize)
    ax.tick_params(axis='both', which='minor', labelsize=labelFontSize)
    title('mus-{}'.format([key for key, value in muscimolSoundTypes.iteritems()][0]))
    behavioranalysis.nice_psycurve_settings(ax, fontsize=10, lineweight=2)

    ax = subplot2grid((2, len(muscimolSessions)), (1, indSession))
    musChordEstimates[indSession, :] = behavioranalysis.plot_psycurve_fit_and_data(muscimolDataObjs[1], 'r')
    ax.tick_params(axis='both', which='major', labelsize=labelFontSize)
    ax.tick_params(axis='both', which='minor', labelsize=labelFontSize)
    title('mus-{}'.format([key for key, value in muscimolSoundTypes.iteritems()][1]))
    behavioranalysis.nice_psycurve_settings(ax, fontsize=10, lineweight=2)

# figtext(0.075, 0.7, 'Fraction of trials going to the right', rotation='vertical')
# figtext(0.4, 0.05, 'Log2(frequency) - octaves')
suptitle(animal)

figure()
for indSession, session in enumerate(salineSessions):
    salineDataObjs, salineSoundTypes = behavioranalysis.load_behavior_sessions_sound_type(animal, [session])

    ax = subplot2grid((2, len(salineSessions)), (0, indSession))
    salineAmpEstimates[indSession, :] = behavioranalysis.plot_psycurve_fit_and_data(salineDataObjs[0], 'k') #The amp_mod session
    ax.tick_params(axis='both', which='major', labelsize=labelFontSize)
    ax.tick_params(axis='both', which='minor', labelsize=labelFontSize)
    title('sal-{}'.format([key for key, value in salineSoundTypes.iteritems()][0]))
    behavioranalysis.nice_psycurve_settings(ax, fontsize=10, lineweight=2)

    ax = subplot2grid((2, len(salineSessions)), (1, indSession))
    salineChordEstimates[indSession, :] = behavioranalysis.plot_psycurve_fit_and_data(salineDataObjs[1], 'k')
    ax.tick_params(axis='both', which='major', labelsize=labelFontSize)
    ax.tick_params(axis='both', which='minor', labelsize=labelFontSize)
    title('sal-{}'.format([key for key, value in salineSoundTypes.iteritems()][1]))
    behavioranalysis.nice_psycurve_settings(ax, fontsize=10, lineweight=2)

# figtext(0.075, 0.7, 'Fraction of trials going to the right', rotation='vertical')
# figtext(0.4, 0.05, 'Log2(frequency) - octaves')
plt.subplots_adjust(wspace = 0.25, hspace = 0.25)
show()
suptitle(animal)


#We should be using nonparametric stats
from scipy import stats
print(stats.ranksums(salineAmpEstimates[:,1], musAmpEstimates[:,1]))
print(stats.ranksums(salineChordEstimates[:,1], musChordEstimates[:,1]))


sa = salineAmpEstimates[:,1]

ma = musAmpEstimates[:,1]

sc = salineChordEstimates[:,1]

mc = musChordEstimates[:,1]

figure()
subplot(121)
plot(zeros((len(sa), 1)), 1/(4.*sa), 'ko')
plot(ones((len(ma), 1)), 1/(4.*ma), 'ro')
xlim([-1, 2])
gca().set_xticks([0, 1])
gca().set_xticklabels(['saline', 'muscimol'])
ylabel('fraction going to right / octave (1/4b)')
title('amp_mod')
show()

subplot(122)
cla()
plot(zeros((len(sc), 1)), 1/(4.*sc), 'ko')
plot(ones((len(mc[mc_good]), 1)), 1/(4.*mc[mc_good]), 'ro')
xlim([-1, 2])
gca().set_xticks([0, 1])
gca().set_xticklabels(['saline', 'muscimol'])
ylabel('fraction going to right / octave (1/4b)')
title('chords')

show()








## -- Debug -- ##

animalName = 'amod002'
salineSessions = ['20160412a']

bdataObjs, bdataSoundTypes = behavioranalysis.load_behavior_sessions_sound_type(animalName, salineSessions)

bdata = bdataObjs[1]


rightTrials = bdata['choice']==bdata.labels['choice']['right']
freqEachTrial = bdata['targetFrequency']
valid = bdata['valid']

(possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue) = behavioranalysis.calculate_psychometric(rightTrials, freqEachTrial, valid)

clf()
plot(np.log2(possibleValues), fractionHitsEachValue, 'bo')
hold(1)

possibleFreq = np.log2(np.unique(freqEachTrial))
maxFreq = max(possibleFreq)
minFreq = min(possibleFreq)


#Calculating with constraints
# constraints = ( 'Uniform({}, {})'.format(minFreq, maxFreq),'Uniform(0,20)' ,'Uniform(0,1)', 'Uniform(0,1)')
constraints = ( 'Uniform({}, {})'.format(minFreq, maxFreq), 'Uniform(0,1)' ,'Uniform(0,0.2)', 'Uniform(0,0.2)')
estimate = extrastats.psychometric_fit(possibleFreq, nTrialsEachValue, nHitsEachValue, constraints)


xRange = possibleFreq[-1]-possibleFreq[1]
fitxval = np.linspace(possibleFreq[0]-0.1*xRange,possibleFreq[-1]+0.1*xRange,40)

#The fitted points
# fityvals = extrastats.psychfun(fitxval, estimate[0], estimate[1], estimate[2], estimate[3])
fityvals = extrastats.psychfun(fitxval, *estimate)

plot(fitxval, fityvals)



#Gamma dist, with these params is essentially flat from 0 to 100 but rapidly drops to zero at zero
from scipy import stats
from pylab import plot, show, mgrid
x = mgrid[0:100:1000j]
figure()
plot ( x, stats.gamma.pdf ( x, 1.01, scale=2000 ) )
show()

#THis still is not working the way I want it to work
