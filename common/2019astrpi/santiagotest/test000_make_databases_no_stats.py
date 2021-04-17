"""
Make databases (without stats). Either all animals or one animal.
"""

import sys
from jaratoolbox import celldatabase

sys.path.append('..')
import studyparams


# Generate and save database
if 1:
    dbPath = '/data/figuresdata/2019astrpi/testAll.h5'
    subjects = studyparams.ASTR_D1_CHR2_MICE
    basicDB = celldatabase.generate_cell_database_from_subjects(subjects)
    celldatabase.save_hdf(basicDB, dbPath)
    sys.exit()
else:
    subject = 'd1pi048'
    dbPath = '/data/figuresdata/2019astrpi/test{}.h5'.format(subject)
    basicDB = celldatabase.generate_cell_database_from_subjects([subject])
    celldatabase.save_hdf(basicDB, dbPath)
    sys.exit()

'''
# Generate and save database
if 0:
    basicDB = celldatabase.generate_cell_database_from_subjects([subject])
    celldatabase.save_hdf(basicDB, dbPath)
else:
    basicDB = celldatabase.load_hdf(dbPath)
'''
