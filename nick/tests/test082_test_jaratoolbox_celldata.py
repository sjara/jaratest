import pandas as pd
from jaratoolbox import ephyscore
from jaratoolbox import celldatabase
reload(ephyscore)
reload(celldatabase)


# dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase.h5'
# db = pd.read_hdf(dbPath, key='dataframe')
db = celldatabase.generate_cell_database('/home/nick/src/jaratest/common/inforecordings/pinp025_inforec.py')

dbRow = db.ix[0]
oneCell = ephyscore.Cell(dbRow)
amInd = oneCell.get_session_inds('am')

behavData = oneCell.load_behavior_by_index(amInd[0])

ephysData = oneCell.load_ephys_by_index(amInd[0])

allData = oneCell.load('am')



