import os
from jaratoolbox import settings
import numpy as np
import pandas
import imp

def generate_cell_database(inforecPath):
    '''
    Iterates over all sites in an inforec and builds a cell database
    Args:
        inforecPath (str): absolute path to the inforec file
    Returns:
        db (pandas.DataFrame): the cell database
    '''

    inforec = imp.load_source('module.name', inforecPath)
    db = pandas.DataFrame()
    for indExperiment, experiment in enumerate(inforec.experiments):
        for indSite, site in enumerate(experiment.sites):
            clusterDir = 'multisession_exp{}site{}'.format(indExperiment, indSite)
            for tetrode in site.tetrodes:
                clusterStatsFn = 'Tetrode{}_stats.npz'.format(tetrode)
                clusterStatsFullPath = os.path.join(settings.EPHYS_PATH,
                                                    inforec.subject,
                                                    clusterDir,
                                                    clusterStatsFn)
                if not os.path.isfile(clusterStatsFullPath):
                    raise NotClusteredYetError("Experiment {} Site {} Tetrode {} is not clustered".format(indExperiment, indSite, tetrode))
                clusterStats = np.load(clusterStatsFullPath)

                for indc, cluster in enumerate(clusterStats['clusters']):
                    clusterDict = {'tetrode':tetrode,
                                   'cluster':cluster,
                                   'indExperiment':indExperiment,
                                   'indSite':indSite,
                                   'inforecPath':inforecPath,
                                   'nSpikes':clusterStats['nSpikes'][indc],
                                   'isiViolations':clusterStats['isiViolations'][indc]}
                    clusterDict.update(site.cluster_info())
                    db = db.append(clusterDict, ignore_index=True)
    return db

class NotClusteredYetError(Exception):
    pass
