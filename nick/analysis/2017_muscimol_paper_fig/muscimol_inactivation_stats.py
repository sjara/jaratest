import numpy as np
from scipy import stats

dataFn = '/home/nick/data/jarahubdata/figuresdata/2016astr/muscimol_inactivation/muscimol_frac_correct_summary.npz'

dataObj = np.load(dataFn)

data = dataObj['data']
subjects = dataObj['subjects']
conditions = dataObj['conditions']

#data(subject, session, condition)

for indSubject in range(5):
    subDataSal = data[indSubject, :, 0]
    subDataMus = data[indSubject, :, 1]

    print indSubject
    print stats.ranksums(subDataSal, subDataMus)

