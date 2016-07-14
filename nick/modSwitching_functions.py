import os
from jaratoolbox import settings
from jaratoolbox.test.nick import behavioranalysis_vnick as behavioranalysis
from jaratoolbox import extraplots
reload(behavioranalysis)


animalName = 'amod003'
date = '20160417a'

fn = '/home/nick/data/behavior/nick/{0}/{1}_2afc_{2}.h5'.format(animalName, animalName, date)
#fn = '/var/tmp/data/santiago/nick/nick_2afc_20160330a.h5' #Not psycurve
bdata = loadbehavior.BehaviorData(fn)

clf()
if any(bdata['psycurveMode']):
    subplot(221)
    plot_frequency_psycurve_soundtype(bdata, 'amp_mod')
    title('{}, amp_mod'.format(animalName))

    subplot(223)
    plot_frequency_psycurve_soundtype(bdata, 'chords')
    title('{}, chords'.format(animalName))
else:
    subplot(221)
    plot_summary_sound_type(bdata, 'amp_mod')
    title('{}, amp_mod'.format(animalName))

    subplot(223)

    plot_summary_sound_type(bdata, 'chords')
    title('{}, chords'.format(animalName))


subplot(222)
plot_dynamics_sound_type(bdata, 'amp_mod', soundfreq=[8, 32])
title('{}, amp_mod'.format(animalName))

subplot(224)
plot_dynamics_sound_type(bdata, 'chords', soundfreq=[5000, 16000])
title('{}, chords'.format(animalName))

behavFolder = '/home/nick/data/behavior_reports'
figname = '{}_{}.png'.format(animalName, date)
filename = os.path.join(behavFolder, figname)

suptitle(date)

tight_layout()

savefig(filename)



# def percent_correct_sound_type(bdata, soundType):
#     trialsSoundType = bdata['soundType']==bdata.labels['soundType'][soundType]
#     valid = bdata['nValid']
#     rewarded = bdata['nRewarded']
#     validSoundType = valid[trialsSoundType][-1]
#     rewardedSoundType = rewarded[trialsSoundType][-1]
#     averagePerf = float(rewardedSoundType)/validSoundType
#     return averagePerf


############### Multiple Session Summary ###############

def muscimol_plot_sound_type(animal, muscimolSessions, salineSessions, soundType, fontsize=12):
    muscimolData = behavioranalysis.load_many_sessions(animal, muscimolSessions)

    trialsSoundTypeMus = muscimolData['soundType']==muscimolData.labels['soundType'][soundType]
    rightTrialsMus = (muscimolData['choice']==muscimolData.labels['choice']['right'])[trialsSoundTypeMus]
    freqEachTrialMus = muscimolData['targetFrequency'][trialsSoundTypeMus]
    validMus = muscimolData['valid'][trialsSoundTypeMus]


    (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
       calculate_psychometric(rightTrialsMus,freqEachTrialMus,validMus)
    (plineM, pcapsM, pbarsM, pdotsM) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue,
                                                                ciHitsEachValue,xTickPeriod=1)
    plt.xlabel('Frequency (kHz)',fontsize=fontsize)
    plt.ylabel('Rightward trials (%)',fontsize=fontsize)
    extraplots.set_ticks_fontsize(plt.gca(),fontsize)




    setp(plineM, color='r')
    setp(pcapsM, color='r')
    setp(pbarsM, color='r')
    setp(pdotsM, markerfacecolor='r')

    salineData = behavioranalysis.load_many_sessions(animal, salineSessions)

    trialsSoundTypeSal = salineData['soundType']==salineData.labels['soundType'][soundType]
    rightTrialsSal = (salineData['choice']==salineData.labels['choice']['right'])[trialsSoundTypeSal]
    freqEachTrialSal = salineData['targetFrequency'][trialsSoundTypeSal]
    validSal = salineData['valid'][trialsSoundTypeSal]


    (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
       calculate_psychometric(rightTrialsSal,freqEachTrialSal,validSal)
    (plineS, pcapsS, pbarsS, pdotsS) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue,
                                                                ciHitsEachValue,xTickPeriod=1)


    title("{}, {}".format(animal, soundType))

def percent_correct_sound_type(bdata, soundType):
    '''
    Return the average percent correct for a behavior session, limited to a single sound type
    '''
    correctChoiceVec = bdata['outcome']==bdata.labels['outcome']['correct']
    trialsSoundType = bdata['soundType']==bdata.labels['soundType'][soundType]
    correctSoundType = correctChoiceVec[trialsSoundType]
    nRewardedSoundType = sum(correctSoundType)
    valid = bdata['valid']
    validSoundType = valid[trialsSoundType]
    nValidSoundType = sum(validSoundType)
    percentCorrectSoundType = nRewardedSoundType/float(nValidSoundType)
    return percentCorrectSoundType*100

clf()
animal = 'amod003'
muscimolSessions = ['20160413a','20160415a','20160417a', '20160419a']
salineSessions = ['20160412a','20160414a','20160416a', '20160418a']

subplot(221)
muscimol_plot_sound_type(animal, muscimolSessions, salineSessions, 'chords')

subplot(223)
muscimol_plot_sound_type(animal, muscimolSessions, salineSessions, 'amp_mod')


#Overall muscimol and saline performance
muscimolData = behavioranalysis.load_many_sessions(animal, muscimolSessions)
muscimolChords = percent_correct_sound_type(muscimolData, 'chords')
muscimolMod = percent_correct_sound_type(muscimolData, 'amp_mod')

salineData = behavioranalysis.load_many_sessions(animal, salineSessions)
salineChords = percent_correct_sound_type(salineData, 'chords')
salineMod = percent_correct_sound_type(salineData, 'amp_mod')


#Individual session muscimol and saline performance

for indp, pair in enumerate(zip(salineSessions, muscimolSessions)):

    salineFile = loadbehavior.path_to_behavior_data(animal,settings.DEFAULT_EXPERIMENTER,'2afc',pair[0])
    salineData = loadbehavior.BehaviorData(salineFile,readmode='full')

    salineChords = percent_correct_sound_type(salineData, 'chords')
    salineMod = percent_correct_sound_type(salineData, 'amp_mod')

    muscimolFile = loadbehavior.path_to_behavior_data(animal,settings.DEFAULT_EXPERIMENTER,'2afc',pair[1])
    muscimolData = loadbehavior.BehaviorData(muscimolFile,readmode='full')

    muscimolChords = percent_correct_sound_type(muscimolData, 'chords')
    muscimolMod = percent_correct_sound_type(muscimolData, 'amp_mod')

    if indp==0:
        allPerfChords = array([salineChords, muscimolChords])
    else:
        allPerfChords = vstack([allPerfChords, array([salineChords, muscimolChords])])

    if indp==0:
        allPerfMod = array([salineMod, muscimolMod])
    else:
        allPerfMod = vstack([allPerfMod, array([salineMod, muscimolMod])])

## -- Chords performance
subplot(222)
bar([0, 1], [salineChords, muscimolChords], width=0.5, facecolor='w', edgecolor='k', linewidth = 2)
#plot lines
for expt in allPerfChords:
    plot([0.25, 1.25], expt, '0.3', lw=2)

#Plot points
for point in allPerfChords[:,0]:
    plot(0.25, point, 'ko', ms=7)
for point in allPerfChords[:,1]:
    plot(1.25, point, 'ro', ms=7)

xlim([-0.5, 2])
xticks([0.25, 1.25])
ax = gca()
ax.set_xticklabels(['Saline', 'Muscimol'])
ylim([0, 100])
ylabel('Percent Correct')



## -- Amp mod performance
subplot(224)
bar([0, 1], [salineMod, muscimolMod], width=0.5, facecolor='w', edgecolor='k', linewidth = 2)
for expt in allPerfMod:
    plot([0.25, 1.25], expt, '0.3', lw=2)

#Plot points
for point in allPerfMod[:,0]:
    plot(0.25, point, 'ko', ms=7)
for point in allPerfMod[:,1]:
    plot(1.25, point, 'ro', ms=7)

xlim([-0.5, 2])
xticks([0.25, 1.25])
ax = gca()
ax.set_xticklabels(['Saline', 'Muscimol'])
ylim([0, 100])
ylabel('Percent Correct')






#amod002

# muscimolSessions = ['20160413a', '20160415a']
# salineSessions = ['20160412a', '20160414a']
muscimolSessions = ['20160413a']
salineSessions = ['20160412a']
animal = 'amod002'

muscimolData = behavioranalysis.load_many_sessions(animal, muscimolSessions)
salineData = behavioranalysis.load_many_sessions(animal, salineSessions)

soundTypes = ['amp_mod', 'chords']

pc = array([percent_correct_sound_type(salineData,'amp_mod'),
       percent_correct_sound_type(muscimolData, 'amp_mod'),
       percent_correct_sound_type(salineData, 'chords'),
       percent_correct_sound_type(muscimolData, 'chords')
       ])

x = [0, 1, 2, 3]

figure()

from jaratoolbox import colorpalette

sb2 = colorpalette.TangoPalette['Chameleon2']
or2 = colorpalette.TangoPalette['Plum2']


bar(x, pc, color = [or2, 'w', sb2, 'w'], edgecolor = [or2, or2, sb2, sb2], linewidth=3)
hline50 = plt.axhline(50,linestyle=':',color='k',zorder=-1)
hline75 = plt.axhline(75,linestyle=':',color='k',zorder=-1)

ylim([0, 100])







fontsize=12




import pypsignifit
from jaratoolbox import extrastats

muscimolSessions = ['20160413a', '20160415a', '20160417a']
salineSessions = ['20160412a', '20160414a', '20160416a']
animal = 'amod002'

muscimolData = behavioranalysis.load_many_sessions(animal, muscimolSessions)
salineData = behavioranalysis.load_many_sessions(animal, salineSessions)

soundTypes = ['amp_mod', 'chords']

soundType = 'chords'
trialsSoundTypeMusAmp = muscimolData['soundType']==muscimolData.labels['soundType'][soundType]
rightTrialsMusAmp = (muscimolData['choice']==muscimolData.labels['choice']['right'])[trialsSoundTypeMusAmp]
freqEachTrialMusAmp = muscimolData['targetFrequency'][trialsSoundTypeMusAmp]
validMusAmp = muscimolData['valid'][trialsSoundTypeMusAmp]


(possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue) = behavioranalysis.calculate_psychometric(rightTrialsMusAmp, freqEachTrialMusAmp, validMusAmp)

M = pypsignifit.psignidata.BootstrapInference(zip(possibleValues, nHitsEachValue, nTrialsEachValue), sample=True, nafc=1, plotprm={"color": "r", "label": "Condition 0"})

trialsSoundTypeSalAmp = salineData['soundType']==salineData.labels['soundType'][soundType]
rightTrialsSalAmp = (salineData['choice']==salineData.labels['choice']['right'])[trialsSoundTypeSalAmp]
freqEachTrialSalAmp = salineData['targetFrequency'][trialsSoundTypeSalAmp]
validSalAmp = salineData['valid'][trialsSoundTypeSalAmp]

(possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue) = behavioranalysis.calculate_psychometric(rightTrialsSalAmp, freqEachTrialSalAmp, validSalAmp)

S = pypsignifit.psignidata.BootstrapInference(zip(possibleValues, nHitsEachValue, nTrialsEachValue), sample=True, nafc=1, plotprm={"color": "k", "label": "Condition 0"})


figure()
# pypsignifit.psigniplot.plotPMF(B)
pypsignifit.plotMultiplePMFs(M, S)


from jaratoolbox.extrastats import psychometric_fit

trialsSoundTypeSalAmp = salineData['soundType']==salineData.labels['soundType'][soundType]
rightTrialsSalAmp = (salineData['choice']==salineData.labels['choice']['right'])[trialsSoundTypeSalAmp]
freqEachTrialSalAmp = salineData['targetFrequency'][trialsSoundTypeSalAmp]
validSalAmp = salineData['valid'][trialsSoundTypeSalAmp]

(possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue) = behavioranalysis.calculate_psychometric(rightTrialsSalAmp, freqEachTrialSalAmp, validSalAmp)

estimate = psychometric_fit(possibleValues, nHitsEachValue, nTrialsEachValue)







#functions stolen from santiago
def weibull(xval,alpha,beta):
    '''Weibull function
    alpha: bias
    beta: related to slope
    NOTE: this function isnot symmetric
    '''
    return 1 - np.exp(-pow(xval/alpha,beta))

def gaussianCDF(xval,mu,sigma):
    from scipy.stats import norm
    return norm.cdf(xval,mu,sigma)

def logistic(xval,alpha,beta):
    return 1/(1+np.exp(-(xval-alpha)/beta))

def psychfun(xval,alpha,beta,lamb,gamma):
    '''Psychometric function that allowing arbitrary asymptotes.
    alpha: bias
    beta : related to slope
    lamb : lapse term (up)
    gamma: lapse term (down)
    '''
    #return gamma + (1-gamma-lamb)*weibull(xval,alpha,beta)
    #return gamma + (1-gamma-lamb)*gaussianCDF(xval,alpha,beta)
    return gamma + (1-gamma-lamb)*logistic(xval,alpha,beta)

soundType = 'amp_mod'
trialsSoundTypeMusAmp = muscimolData['soundType']==muscimolData.labels['soundType'][soundType]
rightTrialsMusAmp = (muscimolData['choice']==muscimolData.labels['choice']['right'])[trialsSoundTypeMusAmp]
freqEachTrialMusAmp = muscimolData['targetFrequency'][trialsSoundTypeMusAmp]
validMusAmp = muscimolData['valid'][trialsSoundTypeMusAmp]


(possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue) = behavioranalysis.calculate_psychometric(rightTrialsMusAmp, freqEachTrialMusAmp, validMusAmp)

M = pypsignifit.psignidata.BootstrapInference(zip(possibleValues, nHitsEachValue, nTrialsEachValue), sample=True, nafc=1, plotprm={"color": "r", "label": "Condition 0"})

trialsSoundTypeSalAmp = salineData['soundType']==salineData.labels['soundType'][soundType]
rightTrialsSalAmp = (salineData['choice']==salineData.labels['choice']['right'])[trialsSoundTypeSalAmp]
freqEachTrialSalAmp = salineData['targetFrequency'][trialsSoundTypeSalAmp]
validSalAmp = salineData['valid'][trialsSoundTypeSalAmp]

(possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue) = behavioranalysis.calculate_psychometric(rightTrialsSalAmp, freqEachTrialSalAmp, validSalAmp)

S = pypsignifit.psignidata.BootstrapInference(zip(possibleValues, nHitsEachValue, nTrialsEachValue), sample=True, nafc=1, plotprm={"color": "k", "label": "Condition 0"})


figure()
# pypsignifit.psigniplot.plotPMF(B)
pypsignifit.plotMultiplePMFs(M, S)










# constraints = ( 'Uniform(0, 100)','Uniform(0,20)' ,'Uniform(0,20)', 'Uniform(0,100)')
estimate = extrastats.psychometric_fit(possibleValues, nTrialsEachValue, nHitsEachValue, constraints)

# clf()
# pypsignifit.psigniplot.plotPMF(session)
# show()






from extracellpy import behavioranalysis as exbehav

figure()
exbehav.plot_psychcurve_fit(possibleValues, nTrialsEachValue, nHitsEachValue, estimate)
show()


xValues = possibleValues
xRange = xValues[-1]-xValues[1]
fitxval = np.linspace(xValues[0]-0.1*xRange,xValues[-1]+0.1*xRange,40)
def psychfun(xval,alpha,beta,lamb,gamma):
    '''Psychometric function that allowing arbitrary asymptotes.
    alpha: bias
    beta : related to slope
    lamb : lapse term (up)
    gamma: lapse term (down)
    '''
    #return gamma + (1-gamma-lamb)*weibull(xval,alpha,beta)
    #return gamma + (1-gamma-lamb)*gaussianCDF(xval,alpha,beta)
    return gamma + (1-gamma-lamb)*logistic(xval,alpha,beta)

psychfun(fitxval, estimate[0])






muscimolSessions = ['20160413a', '20160415a', '20160417a', '20160419a', '20160421a']
salineSessions = ['20160412a', '20160414a', '20160416a', '20160418a', '20160420a']

# muscimolSessions = ['20160413a', '20160415a', '20160417a', '20160419a', '20160421a','20160422a', '20160423a', '20160424a']
# extraMuscimolSessions = ['20160422a', '20160423a', '20160424a']

animal = 'amod002'



#### Try some stats

allPerfChords, allPerfMod = overall_muscimol_performance(animal, muscimolSessions, salineSessions)



####




plotCols = 4
# plotRows = len(muscimolSessions)
plotRows = max(len(muscimolSessions), len(salineSessions))

clf()

# 2 sound types, muscimol/saline
for indRow in range(plotRows):

    #Plot chords saline
    subplot(plotRows, plotCols, indRow*4+1)

    soundType = 'chords'

    date = salineSessions[indRow]
    fn = '/home/nick/data/behavior/nick/{0}/{1}_2afc_{2}.h5'.format(animal, animal, date)
    #fn = '/var/tmp/data/santiago/nick/nick_2afc_20160330a.h5' #Not psycurve
    bdata = loadbehavior.BehaviorData(fn)
    behavioranalysis.plot_frequency_psycurve_soundtype(bdata, soundType)
    title('{} {}'.format(date, soundType))
    xlabel('')

    #plot chords muscimol
    subplot(plotRows, plotCols, indRow*4+2)

    soundType = 'chords'

    date = muscimolSessions[indRow]
    fn = '/home/nick/data/behavior/nick/{0}/{1}_2afc_{2}.h5'.format(animal, animal, date)
    #fn = '/var/tmp/data/santiago/nick/nick_2afc_20160330a.h5' #Not psycurve
    bdata = loadbehavior.BehaviorData(fn)
    behavioranalysis.plot_frequency_psycurve_soundtype(bdata, soundType)
    title('{} {}'.format(date, soundType))
    xlabel('')

    #plot mod saline
    subplot(plotRows, plotCols, indRow*4+3)

    soundType = 'amp_mod'

    date = salineSessions[indRow]
    fn = '/home/nick/data/behavior/nick/{0}/{1}_2afc_{2}.h5'.format(animal, animal, date)
    #fn = '/var/tmp/data/santiago/nick/nick_2afc_20160330a.h5' #Not psycurve
    bdata = loadbehavior.BehaviorData(fn)
    behavioranalysis.plot_frequency_psycurve_soundtype(bdata, soundType)
    title('{} {}'.format(date, soundType))
    xlabel('')

    # plot mod muscimol
    subplot(plotRows, plotCols, indRow*4+4)

    soundType = 'amp_mod'

    date = muscimolSessions[indRow]
    fn = '/home/nick/data/behavior/nick/{0}/{1}_2afc_{2}.h5'.format(animal, animal, date)
    #fn = '/var/tmp/data/santiago/nick/nick_2afc_20160330a.h5' #Not psycurve
    bdata = loadbehavior.BehaviorData(fn)
    behavioranalysis.plot_frequency_psycurve_soundtype(bdata, soundType)
    title('{} {}'.format(date, soundType))

    xlabel('')

suptitle('saline        -        muscimol          -           saline         -         muscimol')




# muscimolSessions = ['20160413a', '20160415a', '20160417a', '20160419a', '20160421a']
salineSessions = ['20160412a', '20160414a', '20160416a', '20160418a', '20160420a']

muscimolSessions = ['20160413a', '20160415a', '20160417a', '20160419a', '20160421a','20160422a', '20160423a', '20160424a']
# extraMuscimolSessions = ['20160422a', '20160423a', '20160424a']

animal = 'amod002'


salineSessions = ['20160412a', '20160414a']

muscimolSessions = ['20160413a', '20160415a', '20160417a']



plotCols = 4
# plotRows = len(muscimolSessions)
plotRows = max(len(muscimolSessions), len(salineSessions))

clf()

# 2 sound types, muscimol/saline
for indRow in range(len(salineSessions)):

    #Plot chords saline
    subplot(plotRows, plotCols, indRow*4+1)

    soundType = 'chords'

    date = salineSessions[indRow]
    fn = '/home/nick/data/behavior/nick/{0}/{1}_2afc_{2}.h5'.format(animal, animal, date)
    #fn = '/var/tmp/data/santiago/nick/nick_2afc_20160330a.h5' #Not psycurve
    bdata = loadbehavior.BehaviorData(fn)
    behavioranalysis.plot_frequency_psycurve_soundtype(bdata, soundType)
    title('{} {}'.format(date, soundType))
    xlabel('')

    subplot(plotRows, plotCols, indRow*4+3)

    soundType = 'amp_mod'

    date = salineSessions[indRow]
    fn = '/home/nick/data/behavior/nick/{0}/{1}_2afc_{2}.h5'.format(animal, animal, date)
    #fn = '/var/tmp/data/santiago/nick/nick_2afc_20160330a.h5' #Not psycurve
    bdata = loadbehavior.BehaviorData(fn)
    behavioranalysis.plot_frequency_psycurve_soundtype(bdata, soundType)
    title('{} {}'.format(date, soundType))
    xlabel('')



for indRow in range(len(muscimolSessions)):

    #plot mod saline
    subplot(plotRows, plotCols, indRow*4+2)
    soundType = 'amp_mod'

    date = muscimolSessions[indRow]
    fn = '/home/nick/data/behavior/nick/{0}/{1}_2afc_{2}.h5'.format(animal, animal, date)
    #fn = '/var/tmp/data/santiago/nick/nick_2afc_20160330a.h5' #Not psycurve
    bdata = loadbehavior.BehaviorData(fn)
    behavioranalysis.plot_frequency_psycurve_soundtype(bdata, soundType)
    title('{} {}'.format(date, soundType))

    soundType = 'chords'


    # plot mod muscimol
    subplot(plotRows, plotCols, indRow*4+4)

    date = muscimolSessions[indRow]
    fn = '/home/nick/data/behavior/nick/{0}/{1}_2afc_{2}.h5'.format(animal, animal, date)
    #fn = '/var/tmp/data/santiago/nick/nick_2afc_20160330a.h5' #Not psycurve
    bdata = loadbehavior.BehaviorData(fn)
    behavioranalysis.plot_frequency_psycurve_soundtype(bdata, soundType)
    title('{} {}'.format(date, soundType))
    xlabel('')


    xlabel('')

suptitle('saline        -        muscimol          -           saline         -         muscimol')




#### 20160429 - evaluating effects of left and right unilateral lesions

figure()
mod_switching_summary('amod002', '20160425a') #right

figure()
mod_switching_summary('amod002', '20160426a') #right

figure()
mod_switching_summary('amod002', '20160427a') #left

figure()
mod_switching_summary('amod002', '20160428a') #right

figure()
mod_switching_summary('amod002', '20160429a') #left

figure()
mod_switching_summary('amod002', '20160430a') #Bilateral

figure()
mod_switching_summary('amod002', '20160501a') #Bilateral
# Bilateral injection tomorrow, then saline, then marking
figure()
mod_switching_summary('amod002', '20160502a') #Bilateral



figure()
mod_switching_summary('amod003', '20160425a') #right

figure()
mod_switching_summary('amod003', '20160426a') #right

figure()
mod_switching_summary('amod003', '20160427a') #left

figure()
mod_switching_summary('amod003', '20160428a') #right

figure()
mod_switching_summary('amod003', '20160429a') #left

figure()
mod_switching_summary('amod003', '20160430a') #Bilateral

figure()
mod_switching_summary('amod003', '20160501a') #Bilateral
# Bilateral injection tomorrow, then saline, then marking
figure()
mod_switching_summary('amod003', '20160502a') #Bilateral


figure()
mod_switching_summary('amod004', '20160429a') #left

figure()
mod_switching_summary('amod004', '20160427a') #left

figure()
mod_switching_summary('amod004', '20160428a') #left

figure()
mod_switching_summary('amod004', '20160430a') #left

figure()
mod_switching_summary('amod004', '20160501a') #left


figure()
mod_switching_summary('amod004', '20160502a') #left

figure()
mod_switching_summary('amod004', '20160503a') #left

figure()
mod_switching_summary('amod004', '20160510a') #left

figure()

#NOTE THE B AFTER 20160504
behavior_summary('adap023', ['20160426a', '20160427a','20160428a','20160429a',   '20160430a', '20160501a', '20160502a', '20160503a', '20160504b','20160505a','20160506a','20160507a','20160508a','20160509a', '20160510a']) #left

figure()
behavioranalysis.behavior_summary('adap023', ['20160511a','20160512a', '20160513a', '20160514a', '20160515a', '20160516a', '20160517a'], trialslim=[0, 1000]) #left

figure()
behavioranalysis.mod_switching_summary('amod004', '20160510a') #left
figure()
behavioranalysis.mod_switching_summary('amod004', '20160511a') #left

figure()
behavioranalysis.mod_switching_summary('amod004', '20160511a') #left

figure()
behavioranalysis.mod_switching_summary('amod004', '20160515a') #left

behavioranalysis.mod_switching_report(['amod004'], ['20160512a','20160513a', '20160514a', '20160515a', '20160516a', '20160517a', '20160518a', '20160519a'], '')
gcf().subplots_adjust(hspace = 0.7)
show()

#### Making plot of average performance across time

clf()

## Settings for amod002 and amod003
# animal = 'amod003'
# sessions = ['20160412a', '20160413a', '20160414a', '20160415a', '20160416a', '20160417a', '20160418a', '20160419a', '20160420a', '20160421a', '20160422a', '20160423a', '20160424a', '20160425a', '20160426a', '20160427a', '20160428a', '20160429a', '20160430a', '20160501a', '20160502a']
# muscimol = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1]

# ## - Amod001 settings - I actually cant use these yet because the data format is different
# animal = 'amod001'
# sessions = ['20160323a', '20160322a', '20160321a', '20160320a', '20160319a', '20160318a', '20160317a', '20160316a', '20160315a', '20160314a']
# muscimol = [1, 0, 0, 1, 0, 1, 0, 1, 0, 1]

## - amod004 settings
clf()
animal = 'amod004'
sessions = ['20160426a','20160427a','20160428a','20160429a','20160430a','20160501a','20160502a','20160503a','20160504a','20160505a','20160506a','20160507a','20160508a','20160509a']
muscimol = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]



modPerf = []
chordPerf = []
modRewarded = []
modValid = []
chordRewarded = []
chordValid = []

for session in sessions:
    bdata = behavioranalysis.load_many_sessions(animal, [session])
    modP, nRewMod, nValMod = behavioranalysis.percent_correct_sound_type(bdata, 'amp_mod')
    chordP, nRewChords, nValChords = behavioranalysis.percent_correct_sound_type(bdata, 'tones')
    modPerf.append(modP)
    chordPerf.append(chordP)
    modRewarded.append(nRewMod)
    modValid.append(nValMod)
    chordRewarded.append(nRewChords)
    chordValid.append(nValChords)

from statsmodels.stats.proportion import proportion_confint

modCis = np.array(proportion_confint(array(modRewarded), array(modValid), method = 'wilson'))
chordCis = np.array(proportion_confint(array(chordRewarded), array(chordValid), method = 'wilson'))

# plot(modPerfs, 'g-o')
# hold(1)
# plot(chordPerfs, 'b-o')
# axhline(y=50, color='0.7')

xvals = range(len(muscimol))

upperModWhisker = modCis[1,:]-modPerf
lowerModWhisker = modPerf-modCis[0,:]
modError = np.vstack((upperModWhisker, lowerModWhisker))

(plineMod, pcapsMod, pbarsMod) = plt.errorbar(xvals, 100*array(modPerf),
                                        yerr = 100*modError,color='g')
pdotsMod = plt.plot(xvals, 100*array(modPerf), 'o',mec='none',mfc='g',ms=8, label='amp_mod')

upperChordWhisker = chordCis[1,:]-chordPerf
lowerChordWhisker = chordPerf-chordCis[0,:]
(plineChord, pcapsChord, pbarsChord) = plt.errorbar(xvals, 100*array(chordPerf),
                                        yerr = [100*lowerChordWhisker, 100*upperChordWhisker],color='b')
pdotsChord = plt.plot(xvals, 100*array(chordPerf), 'o',mec='none',mfc='b',ms=8, label='tones')

legend()

mLabels = ['M' if x==1 else 'S' for x in muscimol ]

ax = gca()
ax.set_xticks(range(len(mLabels)))

# ax.set_xticklabels(mLabels)
ax.set_xticklabels(sessions, rotation=40, ha='right')

colors = {0:'k', 1:'r'}

[label.set_color(colors[mus]) for label,mus in zip(plt.gca().get_xticklabels(), muscimol)]

xlim([-0.5, len(muscimol)-0.5])
ylim([40, 110])

yticks([50, 60, 70, 80, 90, 100])

axhline(50, color = '0.7')
axhline(100, color = '0.7')
margins(0.2)
plt.subplots_adjust(bottom=0.2)
title(animal)
ylabel('Average Percent Correct')
show()




#### Need to start moving towards loading the data already split by sound type and then using generic fxns from behavioranalysis and extraplots

animal = 'amod002'

dataObjs, dataSoundTypes = behavioranalysis.load_behavior_sessions_sound_type(animal, ['20160421a'])

for bdata in dataObjs

bdata = dataObjs[0]
hitTrials = bdata['choice']==bdata.labels['choice']['right']
paramValueEachTrial = bdata['targetFrequency']
valid = bdata['valid']

(possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue) = behavioranalysis.calculate_psychometric(hitTrials, paramValueEachTrial, valid)


clf()
extraplots.plot_psychometric(possibleValues,fractionHitsEachValue,ciHitsEachValue)



