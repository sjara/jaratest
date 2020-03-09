import os
import numpy as np

from jaratoolbox import celldatabase
from jaratoolbox import settings

import database_bandwidth_tuning_fit_funcs as fitfuncs

import figparams
import studyparams

dbFilename = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'photoidentification_cells.h5')
db = celldatabase.load_hdf(dbFilename)

figName = 'supplement_figure_characterisation_of_responses_pure_tone_fit'

dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, figName)

# -- find PV, SOM, and non-SOM cells that are tuned to frequency and with a good centre frequency selected and have sustained sound response
bestCells = db.query(studyparams.SINGLE_UNITS)
bestCells = bestCells.query(studyparams.GOOD_CELLS)

sustPVCells = bestCells.query(studyparams.PV_CELLS)
sustSOMCells = bestCells.query(studyparams.SOM_CELLS)
sustExCells = bestCells.query(studyparams.EXC_CELLS)

# -- get raw data facillitation --

rawPVsustainedFacilitation = sustPVCells['sustainedFacilitationIndexPureTone']
rawSOMsustainedFacilitation = sustSOMCells['sustainedFacilitationIndexPureTone']
rawExsustainedFacilitation = sustExCells['sustainedFacilitationIndexPureTone']


# -- get facillitation and pt vs wn comparison from fit and also raw pt vs wn--
testBands = np.linspace(0,6,500)

PVfitFacilitation = np.zeros(len(sustPVCells))
PVfitPTindex = np.zeros_like(PVfitFacilitation)
rawPVPTindex = np.zeros_like(PVfitFacilitation)

for indRow, (dbIndex, dbRow) in enumerate(sustPVCells.iterrows()):
    PVfitResponse = fitfuncs.diff_gauss_form(testBands, dbRow['mPureTone'], dbRow['R0PureTone'], dbRow['sigmaDPureTone'], dbRow['sigmaSPureTone'], dbRow['RDPureTone'], dbRow['RSPureTone'])
    PVfitFacilitation[indRow] = (max(PVfitResponse)-PVfitResponse[0])/max(PVfitResponse)
    PVfitPTindex[indRow] = (PVfitResponse[0]-PVfitResponse[-1])/(PVfitResponse[0]+PVfitResponse[-1])
    #PVfitPTindex[indRow] = (PVfitResponse[0]-PVfitResponse[-1])/(PVfitResponse[0])
    
    PVsustainedResponse = dbRow['bandwidthSustainedSpikeArrayHighAmp']
    rawPVPTindex[indRow] = (PVsustainedResponse[0]-PVsustainedResponse[-1])/(PVsustainedResponse[0]+PVsustainedResponse[-1])
    #rawPVPTindex[indRow] = (PVsustainedResponse[0]-PVsustainedResponse[-1])/(PVsustainedResponse[0])
    

SOMfitFacilitation = np.zeros(len(sustSOMCells))
SOMfitPTindex = np.zeros_like(SOMfitFacilitation)
rawSOMPTindex = np.zeros_like(SOMfitFacilitation)

for indRow, (dbIndex, dbRow) in enumerate(sustSOMCells.iterrows()):
    SOMfitResponse = fitfuncs.diff_gauss_form(testBands, dbRow['mPureTone'], dbRow['R0PureTone'], dbRow['sigmaDPureTone'], dbRow['sigmaSPureTone'], dbRow['RDPureTone'], dbRow['RSPureTone'])
    SOMfitFacilitation[indRow] = (max(SOMfitResponse)-SOMfitResponse[0])/max(SOMfitResponse)
    SOMfitPTindex[indRow] = (SOMfitResponse[0]-SOMfitResponse[-1])/(SOMfitResponse[0]+SOMfitResponse[-1])
    #SOMfitPTindex[indRow] = (SOMfitResponse[0]-SOMfitResponse[-1])/(SOMfitResponse[0])
    
    SOMsustainedResponse = dbRow['bandwidthSustainedSpikeArrayHighAmp']
    rawSOMPTindex[indRow] = (SOMsustainedResponse[0]-SOMsustainedResponse[-1])/(SOMsustainedResponse[0]+SOMsustainedResponse[-1])
    #rawSOMPTindex[indRow] = (SOMsustainedResponse[0]-SOMsustainedResponse[-1])/(SOMsustainedResponse[0])


ExfitFacilitation = np.zeros(len(sustExCells))
ExfitPTindex = np.zeros_like(ExfitFacilitation)
rawExPTindex = np.zeros_like(ExfitFacilitation)

for indRow, (dbIndex, dbRow) in enumerate(sustExCells.iterrows()):
    ExfitResponse = fitfuncs.diff_gauss_form(testBands, dbRow['mPureTone'], dbRow['R0PureTone'], dbRow['sigmaDPureTone'], dbRow['sigmaSPureTone'], dbRow['RDPureTone'], dbRow['RSPureTone'])
    ExfitFacilitation[indRow] = (max(ExfitResponse)-ExfitResponse[0])/max(ExfitResponse)
    ExfitPTindex[indRow] = (ExfitResponse[0]-ExfitResponse[-1])/(ExfitResponse[0]+ExfitResponse[-1])
    #ExfitPTindex[indRow] = (ExfitResponse[0]-ExfitResponse[-1])/(ExfitResponse[0])
    
    ExsustainedResponse = dbRow['bandwidthSustainedSpikeArrayHighAmp']
    rawExPTindex[indRow] = (ExsustainedResponse[0]-ExsustainedResponse[-1])/(ExsustainedResponse[0]+ExsustainedResponse[-1])
    #rawExPTindex[indRow] = (ExsustainedResponse[0]-ExsustainedResponse[-1])/(ExsustainedResponse[0])

rawExPTindex = rawExPTindex[~np.isnan(rawExPTindex)] # some values end up as nan

# -- save stats --
outputFile = 'facilitation_stats.npz'
outputFullPath = os.path.join(dataDir,outputFile)
np.savez(outputFullPath,
         PVfitFacilitation = PVfitFacilitation, PVfitPTindex = PVfitPTindex, rawPVPTindex = rawPVPTindex, rawPVsustainedFacilitation = rawPVsustainedFacilitation,
         SOMfitFacilitation = SOMfitFacilitation, SOMfitPTindex = SOMfitPTindex, rawSOMPTindex = rawSOMPTindex, rawSOMsustainedFacilitation = rawSOMsustainedFacilitation,
         ExfitFacilitation = ExfitFacilitation, ExfitPTindex = ExfitPTindex, rawExPTindex = rawExPTindex, rawExsustainedFacilitation = rawExsustainedFacilitation)
print outputFile + " saved"

    