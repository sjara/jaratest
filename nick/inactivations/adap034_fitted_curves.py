from jaratest.nick.behavior import behavioranalysis_vnick as bnick
from jaratoolbox import behavioranalysis
import matplotlib.pyplot as plt

animal = 'adap034'
muscimolSessions = ['20170115a']
salineSessions = ['20170114a']

mdata = behavioranalysis.load_many_sessions(animal, muscimolSessions)
sdata = behavioranalysis.load_many_sessions(animal, salineSessions)

# plt.clf()
# bnick.plot_psycurve_fit_and_data(sdata, 'k')
# plt.hold(1)
# bnick.plot_psycurve_fit_and_data(mdata, 'r')
# plt.show()


#Is the change in overall percent correct significant?

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
    # return nCorrect/float(nValid)
    return nCorrect, nValid

ncs, nvs = frac_correct(sdata)
ncm, nvm = frac_correct(mdata)

nis = nvs - ncs
nim = nvm - ncm

from scipy.stats import fisher_exact

oddsratio, pval = fisher_exact([[ncs, nis], [ncm, nim]])

print oddsratio
print pval

