import os
from jaratoolbox import settings
from jaratoolbox import celldatabase
import studyparams

subjects = studyparams.SUBJECTS
for subject in subjects:
    inforecFile = os.path.join(settings.INFOREC_PATH, f'{subject}_inforec.py')

    celldb = celldatabase.generate_cell_database(inforecFile)

    dbPath = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME)
    dbFilename = os.path.join(dbPath, f'celldb_{subject}.h5')

    celldatabase.save_hdf(celldb, dbFilename)
