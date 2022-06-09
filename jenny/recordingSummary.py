import os
import numpy as np
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
import csv

#subject = 'feat008'

print('enter subject name')
subject = input()

dbPath = os.path.join(settings.DATABASE_PATH, f'celldb_{subject}.h5')

celldb = celldatabase.load_hdf(dbPath)
summaryPath = os.path.join(settings.FIGURES_DATA_PATH, 'cell_reports', 'feat_recording_summary.txt')

myFile = open(summaryPath, 'a')
#get unique sessions: index using recording track as these will be unique for each session within an animal
possibleSessions = np.unique(celldb.recordingTrack)
for indSess, thisSess in enumerate(possibleSessions):
    session = possibleSessions[indSess]
    sessCells = celldb.recordingTrack == possibleSessions[indSess]
    numCells = np.sum(sessCells)
    numAud_v = np.sum(sessCells & celldb.recordingSiteName.str.contains('Ventral auditory area'))
    numAud_post = np.sum(sessCells & celldb.recordingSiteName.str.contains('Posterior auditory area'))
    numA1 = np.sum(sessCells & celldb.recordingSiteName.str.contains('Primary auditory area'))
    numAud_d = np.sum(sessCells & celldb.recordingSiteName.str.contains('Dorsal auditory area'))


    myFile.write(f'\n {subject}, {session}, TotalCells:{numCells}, A1:{numA1}, Aud_d:{numAud_d}, Aud_v:{numAud_v}, Aud_post:{numAud_post}')


myFile.close()
