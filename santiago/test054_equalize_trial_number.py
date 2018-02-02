'''
Example of how to find an (equalize) subset of trials.
'''

import numpy as np
from matplotlib import pyplot as plt
from jaratoolbox import behavioranalysis
reload(behavioranalysis)

# -- Create simulated trialsEachCond --
np.random.seed(0)
nCond = 6
nTrials = 60
randtemp = np.random.rand(nTrials,nCond)
randtemp += 0.15*np.arange(nCond)
trialsEachCond = np.zeros((nTrials,nCond), dtype=bool)
for indt in range(nTrials):
    maxind = np.argmax(randtemp[indt,:])
    trialsEachCond[indt, maxind] = True
# --- end of creating trialsEachCond ---

    
fraction = 0.25

newTrialsEachCond = behavioranalysis.subset_trials_equalized(trialsEachCond, fraction)


# -- Plot results --
plt.clf()
if 0:
    plt.bar(np.arange(len(equalizedTrialCount)), equalizedTrialCount)
    plt.title('Total = {}'.format(np.sum(equalizedTrialCount)))
else:
    plt.subplot(1,2,1)
    plt.imshow(trialsEachCond, interpolation='nearest')
    plt.title('Original')
    plt.subplot(1,2,2)
    plt.imshow(newTrialsEachCond, interpolation='nearest')
    plt.title('Equalized subset')
plt.show()
