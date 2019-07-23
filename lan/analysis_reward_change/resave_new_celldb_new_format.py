import os
import pandas as pd
from jaratoolbox import celldatabase

animals = ['adap005', 'adap012', 'adap013', 'adap015', 'adap017', 'gosi001', 'gosi004', 'gosi008', 'gosi010', 'adap067', 'adap071']
celldbFolder = '/home/languo/data/database/new_celldb'

for animal in animals:
	celldbPath = os.path.join(celldbFolder, '{}_database_old_format.h5'.format(animal))
	celldb = pd.read_hdf(celldbPath, key='reward_change')
	newCelldbPath = os.path.join(celldbFolder, '{}_database.h5'.format(animal))
	print('resaving celldb as {}'.format(newCelldbPath))
	celldatabase.save_hdf(celldb, newCelldbPath)