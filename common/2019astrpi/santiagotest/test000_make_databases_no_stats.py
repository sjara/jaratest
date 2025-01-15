"""
Make databases (without stats). Either all animals or one animal.

NOTE: the databases by Devin included cells with only one spike (infinite quality).
      and 4428 total number of cells
The new celldatabase fixed this, but then the cell indices get out of sync.
When generating the database, we comment a couple of lines in celldatabase (391-392)
to replicate the older DB to be able to use cell_indices_manually_removed.txt
"""

import sys
from jaratoolbox import celldatabase

sys.path.append('..')
import studyparams

from importlib import reload
reload(celldatabase)


# Generate and save database
if 1:
    #dbPath = '/data/figuresdata/2019astrpi/testAll.h5'
    dbPath = '/tmp/sj_all_cells_20211211.h5'
    #dbPath = '/tmp/testAll2.h5'
    subjects = studyparams.ASTR_D1_CHR2_MICE
    basicDB = celldatabase.generate_cell_database_from_subjects(subjects, onlygood=True)
    celldatabase.save_hdf(basicDB, dbPath)
    sys.exit()
else:
    subject = 'd1pi048'
    #dbPath = '/data/figuresdata/2019astrpi/test{}.h5'.format(subject)
    dbPath = '/tmp/test{}.h5'.format(subject)
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
