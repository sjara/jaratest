from jaratest.nick.inactivations import muscimolSessions
reload(muscimolSessions)
from jaratoolbox import behavioranalysis
from matplotlib import pyplot as plt
from jaratoolbox import colorpalette
from scipy import stats

animalsToUse = ['adap023',
                'adap028',
                'adap029',
                'adap021',
                'adap032',
                'adap033',
                'adap035']

animalColor = {'adap023': colorpalette.TangoPalette['Butter1'],
                'adap028': colorpalette.TangoPalette['Chameleon1'],
                'adap029': colorpalette.TangoPalette['Orange2'],
                'adap021': colorpalette.TangoPalette['SkyBlue1'],
                'adap032': colorpalette.TangoPalette['Plum1'],
                'adap033': colorpalette.TangoPalette['Chocolate2'],
                'adap035': colorpalette.TangoPalette['ScarletRed1']}

def frac_correct(bdata, ci=False):
    '''
    Calculate the fraction of correct trials overall for a bdata object.

    Args:
        bdata (jaratoolbox.loadbehavior.BehaviorData dict): the behavior data to use
        ci (bool): whether to calculate confidence intervals
    Returns:
        fractionCorrect (float): the fraction of correct trials
        confInt (array): upper and lower confidence intervals
    '''
    correct = bdata['outcome']==bdata.labels['outcome']['correct']
    nCorrect = sum(correct)
    valid = bdata['valid']
    nValid = sum(valid)
    fractionCorrect = nCorrect/float(nValid)
    if ci:
        from statsmodels.stats.proportion import proportion_confint
        confInt = np.array(proportion_confint(nCorrect, nValid, method = 'wilson'))
        return fractionCorrect, confInt
    else:
        return fractionCorrect

plt.clf()

allSaline = []
allMus = []

for animal in animalsToUse:
    musSessions = muscimolSessions.animals[animal]['muscimol']
    salSessions = muscimolSessions.animals[animal]['saline']
    musBdata = behavioranalysis.load_many_sessions([animal], musSessions)
    salBdata = behavioranalysis.load_many_sessions([animal], salSessions)

    musPercentCorrect = 100*frac_correct(musBdata)
    salPercentCorrect = 100*frac_correct(salBdata)

    allSaline.append(salPercentCorrect)
    allMus.append(musPercentCorrect)

    plt.plot([0, 1], [salPercentCorrect, musPercentCorrect], '-o', color=animalColor[animal], mec=animalColor[animal], ms=8, lw=1)
    plt.hold(1)

plt.xlim([-0.5, 1.5])
plt.ylim(0, 100)
plt.axhline(y=50, ls='--', color='0.8')
plt.ylabel('Percent correct')
ax = plt.gca()
ax.set_xticks([0, 1])
ax.set_xticklabels(['Saline', 'Muscimol'])

print stats.ranksums(allSaline, allMus)
