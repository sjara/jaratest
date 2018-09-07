'''
We need to move any processed data out of the histology folder for each mouse into a folder like test000_processed.
Anything that is not a CZI file should not be in the test000 folder, but should be outside. 
'''

import os
import pprint
ANATOMY_DIR = '/mnt/jarahubdata/jarashare/histology'

paths = []

for dirpath, dirnames, filenames in os.walk(ANATOMY_DIR):
    nonCZI = [s for s in filenames if '.czi' not in s]
    if len(nonCZI)>0:
        paths.append(dirpath)

pprint.pprint(sorted(paths))
