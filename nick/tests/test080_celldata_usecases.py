'''
#celldatabase
def get_cell_info(subject, date, depth, tetrode, cluster, session):
    return (subject, date, tetrode, cluster, ephysSession, behavSession)

#ephyscore
def load_session_for_one_cell(subject, date, tetrode, cluster, ephysSession, behavSession):
    return (spikeData, eventData, bdata)

def get_session_inds(cell, sessiontype)
    #Gets ALL the indices where the list of sessiontypes == sessiontype
    sessionInds = [i for i, st in enumerate(cell['sessiontype']) if st==sessiontype]

def get_cell_info_fromframe(dataframe, indCell, session='', sessionind=None):

    #Specify either the sessiontype string or the index of the session in the list. If neither, fail. If both, we don't know what behavior to have right now. If you specify session='am' and sessionInd = 1, it isn't supposed to 


    cell = dataframe.ix[indCell]
    subject = cell['cell']
    date = cell['date']
    tetrode = int(cell['tetrode']) #FIXME: Remove the int() when we solve the problem that converts them to floats
    cluster = int(cell['cluster']) #FIXME: Remove the int() when we solve the problem that converts them to floats

    return (subject, date, tetrode, cluster, ephysSession, behavSession)
'''
from jaratoolbox import ephyscore
from jaratoolbox import celldatabase

###### ------ Report for each cell in a database, plus selecting which session of type to use ----- ####
#TODO: Multi session for one cell

dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase.h5'
db = pd.read_hdf(dbPath, key='dataframe')

# Select the good, isolated cells from the database
goodCells = db.query('isiViolations < 0.02')

for indCell, cell in goodCells.iterrows():
    #Get the ephys data/behavior data
    cellObj = ephyscore.CellDataObj(cell)

    #AM session
    #Find the inds for a specific sessiontype that was recorded several times
    sessionInds = cellObj.find_session_inds('am')
    for sessionInd in sessionInds:
        #Get the bdata for this session
        bdata = cellObj.get_behavior_by_index(sessionInd)
        #Look at something in the bdata
        if bdata['something']==whatWeWant:
            indToUse=sessionInd
            break #We keep this bdata and use this sessionInd
    #get the spikeData for this ind (we might already have the bdata because we just loaded it)
    ephysData = cellObj.load_ephys_by_ind(sessionInd)

    #Noiseburst session

    #Plot report with the data


####### -------- Figure of an example cell -------- #########

#Which cell to get?
cellDict = {'subject' : 'pinp025',
            'date' : '2017-10-25',
            'depth' : 1000,
            'tetrode' : 7,
            'cluster' : 2}
#TODO: Which penetration from this date?

#TODO: Use settings here
dbPath = '/mnt/jarahubdata/figuresdata/2018thstr/celldatabase.h5'
db = pd.read_hdf(dbPath, key='dataframe')

# Get the row for the cell you want from the dataframe (include things like spikeshape, depth)

cell = celldatabase.find_cell(db, **cellDict)
cellObj = ephyscore.CellDataObject(cell)

# Load ephys/behavior data for the cell

# Do some analysis

# Plot something


####### -------- Plot summary figure for paper -------- #########

dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase.h5'
db = pd.read_hdf(dbPath, key='dataframe')

# Select the good, isolated cells from the database
goodCells = db.query('isiViolations < 0.02')

#Options for selecting subdatabases
# thalamusDB = goodCells.query("brainarea == '{}' and nSpikes > 100".format(mybrainarea))
# thalamusDB = goodCells.query("brainarea == '@mybrainarea' and nSpikes > 100")
# thalamusDB = goodCells[(goodCells['brainarea'] == mybrainarea) & (goodCells)]

# Select the cells from the thalamus
mybrainarea = 'rightThal'
brainareaDB = goodCells.query("brainarea == '{}' and nSpikes > 100".format(mybrainarea))

# Do some analysis for both
maxSyncRate = np.empty(len(brainareaDB))
for indIter, (indCell, cell) in enumerate(brainareaDB.iterrows()):

    #cellObj = CellDataObj(thalamusDB, indCell) #Rare for us to only have/use the index for a cell
    #cellObj = CellDataObj(subject, date, ...)
    #cellObj = CellDataObj(cell)
    cellObj = CellDataObj(cell)

    #Load ephys and behavior for AM session
    # amInd = cellObj.get_last_session_ind('am')
    # Old
    # spikeData, eventData, bdata = cellObj.load('am')
    # eventOnsetTimes = eventData.get_event_onset_times()
    ephysData, behavData = cellObj.load('am')
    eventOnsetTimes = ephysData['events']['stimOn']

    #Calculate vector strength for each AM rate
    rateEachTrial = behavData['CurrentFreq']
    maxSyncRateOneCell = vector_strength(ephysData['spiketimes'], eventOnsetTimes, rateEachTrial)
    maxSyncRate[indIter] = maxSyncRateOneCell

# Plot histograms
hist(maxSyncRate) #is an array of floats of length nCells Thalamus

###### -------- Calculate and save a feature for many cells in the dataframe -------- ########
# Save the dataframe with the column you calculated in the previous example
# Keep the original clean database and a processed one

'''

for indCell, cell in goodCells.iterrows():

    #We may convert all of this to one list and use * to pass to the next loading function
    subject, date, tetrode, ephysSession, behavSession = get_cell_info_fromframe(goodCells, indCell)

    #Get the ephys data/behavior data
    spikeData, eventData, bdata = load_session_for_one_cell(subject,
                                                            date,
                                                            tetrode,
                                                            ephysSession,
                                                            behavSession)

    #Select which 'bandwidth' session to use for the cell, since it has multiple

    #Calculate a feature for the cell

    #Add the calculated feature to the dataframe
'''
