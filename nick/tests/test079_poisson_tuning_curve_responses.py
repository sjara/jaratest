# I think that the responses we see when recording from cells during tuning curves are pretty zero-heavy, which influences the statistics that we will use. For instance, the std of some baselines is very high while the mean is very small because of many zeros.

import pandas as pd
from jaratoolbox import ephyscore

def find_cell(dataframe, subject, date, depth, tetrode, cluster):
    cell = dataframe.query("subject==@subject and date==@date and depth==@depth and tetrode==@tetrode and cluster==@cluster")
    if len(cell)==1:
        return cell.iloc[0] #Return just the first row as a Series
    else:
        print "WARNING: Multiple rows met these criteria - returning all the rows"
        return cell #Return the whole result dataframe

dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase.h5'
db = pd.read_hdf(dbPath, key='dataframe')

cellDict = {'subject':'pinp017',
        'date':'2017-03-23',
        'depth':1281,
        'tetrode':7,
        'cluster':2}

cell = find_cell(db, cellDict['subject'], cellDict['date'], cellDict['depth'], cellDict['tetrode'], cellDict['cluster'])
cellDict = cell.to_dict()
cellData = ephyscore.CellData(**cellDict)

