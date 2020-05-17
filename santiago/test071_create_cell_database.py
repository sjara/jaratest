'''
Testing tools for creating a database of cells.
'''

import os
from jaratoolbox import celldatabase
from jaratoolbox import settings

inforecFile = os.path.join(settings.INFOREC_PATH,'test000_inforec.py')
celldb = celldatabase.generate_cell_database(inforecFile)
