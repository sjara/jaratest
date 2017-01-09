from matplotlib import pyplot as plt
import numpy as np
from jaratest.nick.inactivations import muscimolSessions as ms
from jaratoolbox import behavioranalysis
from jaratest.nick.behavior import behavioranalysis_vnick as bnick
from jaratoolbox import extraplots
from scipy import stats
import matplotlib.pyplot as plt
from statsmodels.stats import proportion

reload(ms)

def load_subject(subject, muscimolSessions, salineSessions):
    muscimolData = behavioranalysis.load_many_sessions(subject, muscimolSessions)
    salineData = behavioranalysis.load_many_sessions(subject, salineSessions)
    return muscimolData, salineData

def set_markeredgewidth(pobjs, markeredgewidth):
    for obj in pobjs:
        obj.set_markeredgewidth(markeredgewidth)

def set_linewidth(pobjs, linewidth):
    for obj in pobjs:
        obj.set_linewidth(linewidth)

def prop_correct(bdata):
    valid = bdata['valid']
    correct = bdata['outcome'] == bdata.labels['outcome']['correct']
    validCorrect = (valid & correct)
    numValid = sum(valid)
    numCorrect = sum(validCorrect)
    ciLow, ciUp = proportion.proportion_confint(numCorrect, numValid)
    propCorr = numCorrect/np.double(numValid)

    return propCorr, ciLow, ciUp, numCorrect, numValid


salPerf = []
salUpper = []
salLower = []

musPerf = []
musUpper = []
musLower = []

pVals = []

linewidth=3
plt.rc('axes', linewidth=2)


plt.clf()
ax = plt.subplot(131)
plt.tick_params(axis='x',
                which='both',
                bottom='off',
                top='off',
                labelbottom='off')
plt.tick_params(axis='y',
                which='both',
                left='off',
                right='off',
                labelleft='off')
muscimolData, salineData = load_subject('adap028',
                  ms.adap028['muscimol0250'],
                  ms.adap028['saline'])

propCorr, ciLow, ciUp, numCorrectSal, numValidSal = prop_correct(salineData)
salPerf.append(propCorr)
salLower.append(ciLow)
salUpper.append(ciUp)

propCorr, ciLow, ciUp, numCorrectMus, numValidMus = prop_correct(muscimolData)
musPerf.append(propCorr)
musLower.append(ciLow)
musUpper.append(ciUp)

ctable = [[numCorrectSal, numValidSal-numCorrectSal], [numCorrectMus, numValidMus-numCorrectMus]]
oddsRatio, pVal = stats.fisher_exact(ctable)
pVals.append(pVal)

pcaps, pbars, pdots = bnick.plot_psycurve_fit_and_data(muscimolData, 'r', linewidth=linewidth, returnHandles=True)
set_markeredgewidth(pcaps, 3)
set_linewidth(pcaps, 3)
set_linewidth(pbars, 3)
plt.hold(True)
pcaps, pbars, pdots = bnick.plot_psycurve_fit_and_data(salineData, 'k', linewidth=linewidth, returnHandles=True)
set_markeredgewidth(pcaps, 3)
set_linewidth(pcaps, 3)
set_linewidth(pbars, 3)
plt.xlabel('')
plt.ylabel('')
extraplots.boxoff(ax)

ax = plt.subplot(132)
plt.tick_params(axis='x',
                which='both',
                bottom='off',
                top='off',
                labelbottom='off')
plt.tick_params(axis='y',
                which='both',
                left='off',
                right='off',
                labelleft='off')
muscimolData, salineData = load_subject('adap029',
                  ms.adap029['muscimol0250'],
                  ms.adap029['saline'])


propCorr, ciLow, ciUp, numCorrectSal, numValidSal = prop_correct(salineData)
salPerf.append(propCorr)
salLower.append(ciLow)
salUpper.append(ciUp)

propCorr, ciLow, ciUp, numCorrectMus, numValidMus = prop_correct(muscimolData)
musPerf.append(propCorr)
musLower.append(ciLow)
musUpper.append(ciUp)

ctable = [[numCorrectSal, numValidSal-numCorrectSal], [numCorrectMus, numValidMus-numCorrectMus]]
oddsRatio, pVal = stats.fisher_exact(ctable)
pVals.append(pVal)


pcaps, pbars, pdots = bnick.plot_psycurve_fit_and_data(muscimolData, 'r', linewidth=linewidth, returnHandles=True)
set_markeredgewidth(pcaps, 3)
set_linewidth(pcaps, 3)
set_linewidth(pbars, 3)
plt.hold(True)
pcaps, pbars, pdots = bnick.plot_psycurve_fit_and_data(salineData, 'k', linewidth=linewidth, returnHandles=True)
set_markeredgewidth(pcaps, 3)
set_linewidth(pcaps, 3)
set_linewidth(pbars, 3)
plt.xlabel('')
plt.ylabel('')
extraplots.boxoff(ax)

ax = plt.subplot(133)
plt.tick_params(axis='x',
                which='both',
                bottom='off',
                top='off',
                labelbottom='off')
plt.tick_params(axis='y',
                which='both',
                left='off',
                right='off',
                labelleft='off')
muscimolData, salineData = load_subject('adap021',
                  ms.adap021['muscimol0250'],
                  ms.adap021['saline_muscimol0250'])


propCorr, ciLow, ciUp, numCorrectSal, numValidSal = prop_correct(salineData)
salPerf.append(propCorr)
salLower.append(ciLow)
salUpper.append(ciUp)

propCorr, ciLow, ciUp, numCorrectMus, numValidMus = prop_correct(muscimolData)
musPerf.append(propCorr)
musLower.append(ciLow)
musUpper.append(ciUp)

ctable = [[numCorrectSal, numValidSal-numCorrectSal], [numCorrectMus, numValidMus-numCorrectMus]]
oddsRatio, pVal = stats.fisher_exact(ctable)
pVals.append(pVal)

pcaps, pbars, pdots = bnick.plot_psycurve_fit_and_data(muscimolData, 'r', linewidth=linewidth, returnHandles=True)
set_markeredgewidth(pcaps, 3)
set_linewidth(pcaps, 3)
set_linewidth(pbars, 3)
plt.hold(True)
pcaps, pbars, pdots = bnick.plot_psycurve_fit_and_data(salineData, 'k', linewidth=linewidth, returnHandles=True)
set_markeredgewidth(pcaps, 3)
set_linewidth(pcaps, 3)
set_linewidth(pbars, 3)
plt.xlabel('')
plt.ylabel('')
extraplots.boxoff(ax)


plt.show()
plt.tight_layout()

salPerf = np.array(salPerf)*100
salLower = np.array(salLower)*100
salUpper = np.array(salUpper)*100

musPerf = np.array(musPerf)*100
musLower = np.array(musLower)*100
musUpper = np.array(musUpper)*100

plt.clf()
ind = np.array([1, 2, 3])
width = 0.35
fig, ax = plt.subplots()
rects1 = ax.bar(ind, salPerf, width, edgecolor='k', facecolor='w',
                linewidth=3,
                yerr=[salPerf - salLower, salUpper-salPerf],
                error_kw={'ecolor': 'k', 'linewidth':2})

rects2 = ax.bar(ind+width+0.015, musPerf, width, edgecolor='r', facecolor='w',
                linewidth=3,
                yerr=[musPerf - musLower, musUpper-musPerf],
                error_kw={'ecolor': 'r', 'linewidth':2})

ax = plt.gca()
ax.set_xticks(ind + width)
ax.set_xticklabels(['Mouse 1', 'Mouse 2', 'Mouse 3'])
plt.ylim([0, 100])
plt.xlim([ind[0]-width, ind[-1]+3*width])
ax.axhline(y=50, color='0.5', ls='--')

extraplots.boxoff(ax)
extraplots.set_ticks_fontsize(ax, 20)

fig = plt.gcf()
fig.set_size_inches(5, 3)
plt.savefig('figs/muscimolPercentCorrect.svg')

plt.show()


