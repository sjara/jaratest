import numpy as np
import pandas as pd
from jaratoolbox import celldatabase

'''
On 2018-09-13, I used this function to consolidate columns from 3 databases into one, and I changed the info column to make it saveable by the new celldatabase.save_hdf() function. The resulting database won't be loadable by the figure code until the celldatabase.load_hdf() function is used. I have tested figure_am.py and figure_frequency.py, which both now work.

'''

initialDB = '/mnt/jarahubdata/figuresdata/2018thstr/celldatabase_ALLCELLS_MODIFIED_CLU.h5'
amDiscrimDB = '/mnt/jarahubdata/figuresdata/2018thstr/figure_am/celldatabase_with_am_discrimination_accuracy.h5'
phaseDiscrimDB = '/mnt/jarahubdata/figuresdata/2018thstr/figure_am/celldatabase_with_phase_discrimination_accuracy.h5'

dbInitial = pd.read_hdf(initialDB, key='dataframe')

# Change the info column to allow saving with the new function
dbInitial['info'] = dbInitial['info'].apply(lambda x: [x] if not isinstance(x, list) else x)

dbAM = pd.read_hdf(amDiscrimDB, key='dataframe')
dbPhase = pd.read_hdf(phaseDiscrimDB, key='dataframe')

# Columns that need to be moved from aux databases to the main database
# dbAM has a column 'accuracy'. This is the discrimination accuracy of AM rate.
# dbPhase has a set of columns called phaseAccuracy_{}Hz for each AM rate

# Rename this column to be more informative. TODO: See what else we need to do if we change this name.
dbInitial['rateDiscrimAccuracy'] = dbAM['accuracy']

possibleRateKeys = np.array([4, 5, 8, 11, 16, 22, 32, 45, 64, 90, 128])
for rate in possibleRateKeys:
    dbInitial['phaseDiscrimAccuracy_{}Hz'.format(rate)] = dbPhase['phaseAccuracy_{}Hz'.format(rate)]

newFn = '/mnt/jarahubdata/figuresdata/2018thstr/celldatabase_calculated_columns.h5'

#Save the database as a new name
celldatabase.save_hdf(dbInitial, newFn)

