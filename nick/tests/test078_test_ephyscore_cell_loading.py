from jaratoolbox import celldatabase
import pandas as pd 
import os
from jaratoolbox import settings
from jaratoolbox import ephyscore
reload(ephyscore)

dbPath = os.path.join(settings.FIGURES_DATA_PATH, '2018thstr', 'celldatabase.h5')
db = pd.read_hdf(dbPath, key='dataframe')

#Select a cell
cell = db.ix[1033]
#Convert the cell to a dict. Or, you can make a dict yourself that has the right fields
cellDict = cell.to_dict()
cellData = ephyscore.CellData(**cellDict)

spikeData, events = cellData.load_ephys('am')
bdata = cellData.load_bdata('am')
