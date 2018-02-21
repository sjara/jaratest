from jaratoolbox import extraplots
from matplotlib import pyplot as plt
from collections import Counter
from jaratoolbox import colorpalette
import numpy as np
import pandas as pd
import figparams

dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase.h5'
db = pd.read_hdf(dbPath, key='dataframe')

soundResponsive = db.query('isiViolations<0.02 and shapeQuality>2 and noisePval<0.05')
thal1 = soundResponsive.groupby('brainarea').get_group('rightThal')
thal2 = soundResponsive.groupby('brainarea').get_group('rightThalamus')
thal = pd.concat([thal1, thal2])
ac = soundResponsive.groupby('brainarea').get_group('rightAC')

tbw = (thal['upperFreq']-thal['lowerFreq'])/thal['cf']
tbw = tbw[pd.notnull(tbw)]

acbw = (ac['upperFreq']-ac['lowerFreq'])/ac['cf']
acbw = acbw[pd.notnull(acbw)]

plt.clf()
plt.subplot(211)
plt.hist(tbw)
plt.xlim([0, 3])
plt.subplot(212)
plt.hist(acbw)
plt.xlim([0, 3])
plt.show()

