"""
Test if dataframe indices get saved by celldatabase.save_hdf()
"""

import numpy as np
import pandas as pd
from jaratoolbox import celldatabase

np.random.seed(0)

dframe = pd.DataFrame(np.eye(6))
dframe.columns = ['one','two','three','four','five','six']
dframe['one'] = np.random.rand(6)

dframe = dframe.query('one<0.55')

celldatabase.save_hdf(dframe, '/tmp/testdb.h5')

newFrame = celldatabase.load_hdf('/tmp/testdb.h5')

