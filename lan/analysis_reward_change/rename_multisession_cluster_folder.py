import os
import imp
from jaratoolbox import settings

inforecFolder = settings.INFOREC_PATH
ephysFolder = settings.EPHYS_PATH_REMOTE

animals = ['gosi001']
for animal in animals:
	inforecPath = os.path.join(inforecFolder, '{}_inforec.py'.format(animal))
	inforec = imp.load_source('inforec_module', inforecPath)
	ephysDirThisAnimal = os.path.join(ephysFolder, animal)
	for experiment in inforec.experiments:
		for inds, site in enumerate(experiment.sites):
			#print inds, site.clusterFolder
			oldMultisessionFolder = os.path.join(ephysDirThisAnimal, 'multisession_exp{}site0'.format(inds))
			newMultisessionFolder = os.path.join(ephysDirThisAnimal, site.clusterFolder)
			if os.path.exists(oldMultisessionFolder):
				print 'renaming {} to {}'.format(oldMultisessionFolder, newMultisessionFolder)
				os.rename(oldMultisessionFolder, newMultisessionFolder) 
			else:
				print 'OLD "experiment" {} missing from clustering!!'
			