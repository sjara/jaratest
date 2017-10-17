#Report

dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase.h5'
db = pd.read_hdf(dbPath, key='dataframe')

for indCell, cell, in db.iterrows():

    cellDict = cell.to_dict()
    cellData = ephyscore.CellData(**cellDict)

    #Phys only
    spikeData, eventData, bdata = cellData.load_ephys('noiseburst')

    #Phys and behavior
    spikeData, eventData, bdata = cellData.load_ephys('am')

    #Spikeshape and parameters
    cell['averageSpikeShape']



#celldatabase
def get_cell_info(subject, date, depth, tetrode, cluster, session):

    return (subject, date, tetrode, cluster, ephysSession, behavSession)

#ephyscore
def load_session_for_one_cell(subject, date, tetrode, cluster, ephysSession, behavSession):

    return (spikeData, eventData, bdata)



