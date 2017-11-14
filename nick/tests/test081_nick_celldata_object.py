# Report - using a CellData object that is initialized using information about a cell

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

