import os
import json
import itertools
from jaratoolbox.test.nick.ephysExperiments import ephys_experiment_v3 as ee3
from jaratoolbox.test.nick.ephysExperiments import physiologyreports
reload(physiologyreports)


def convert_to_builtin_type(obj):
    d = {'__class__': obj.__class__.__name__,
         '__module__': obj.__module__,
         }
    d.update(obj.__dict__)
    return d


class Recording(object):

    '''
    Parent class so that we don't have to re-enter this info for each recording site.
    The construction of new recording sites could possible be handled through a
    method of this class in the future. For now, an instance of this class is a
    required argument for the RecordingSite class
    '''

    def __init__(self, animalName, date, experimenter, paradigm, **kwargs):
        self.animalName = animalName
        self.date = date
        self.experimenter = experimenter
        self.siteList = []
        self.paradigm = paradigm
        # An internal instance of the ephys experiment class for easy plotting?
        self.ee = ee3.EphysExperiment(
            animalName,
            date,
            experimenter=experimenter,
            paradigm=paradigm,
            **kwargs)

    def add_site(self, depth, goodTetrodes):
        site = Site(depth, goodTetrodes, animalName=self.animalName,
                    date=self.date, experimenter=self.experimenter, paradigm=self.paradigm)

        self.siteList.append(site)
        return site


class Site(object):

    '''
    Class for holding information about a recording site. Will act as a parent for all of the
    RecordingSession objects that hold information about each individual recording session.
    '''

    def __init__(self, depth, goodTetrodes, animalName, date, experimenter, paradigm):

        self.animalName = animalName
        self.date = date
        self.experimenter = experimenter
        self.paradigm = paradigm
        self.depth = depth
        self.goodTetrodes = goodTetrodes
        self.sessionList = []
        self.clusterList = []

    def add_session(self, sessionID, behavFileIdentifier, sessionType):
        session = Session(sessionID, behavFileIdentifier, sessionType, self.date)
        self.sessionList.append(session)
        return session

    def add_cluster(
            self,
            clusterNumber,
            tetrode,
            soundResponsive=False,
            laserPulseResponse=False,
            followsLaserTrain=False,
            comments=''):
        cluster = Cluster(
            animalName=self.animalName,
            date=self.date,
            depth=self.depth,
            experimenter=self.experimenter,
            paradigm = self.paradigm,
            clusterNumber=clusterNumber,
            tetrode=tetrode,
            ephysSessionList=self.get_session_filenames(),
            behavFileList=self.get_session_behavIDs(),
            sessionTypes=self.get_session_types(),
            soundResponsive=soundResponsive,
            laserPulseResponse=laserPulseResponse,
            followsLaserTrain=followsLaserTrain,
            comments=comments)
        self.clusterList.append(cluster)
        return cluster

    def get_session_filenames(self):
       return [s.session for s in self.sessionList]

    def get_session_behavIDs(self):
        return [s.behavFileIdentifier for s in self.sessionList]

    def get_session_types(self):
        return [s.sessionType for s in self.sessionList]

    def get_session_inds_one_type(self, plotType, report):
        return [
            index for index,
            s in enumerate(
                self.sessionList) if (
                (s.plotType == plotType) & (
                    s.report == report))]

    def generate_main_report(self, **kwargs):
        '''
        '''
        if self.experimenter=='nick' or self.experimenter=='lan':
            physiologyreports.nick_lan_main_report(self, **kwargs)
            print kwargs

class Session(object):

    '''
    Class to hold information about a single session.
    Includes the session name, the type of session, and any associated behavior data
    Accepts just the time of the recording (i.e. 11-36-54), and the date, which can
    be passed from the parent when this class is called. This keeps us from
    having to write it over and over again.
    '''

    def __init__(self, sessionID, behavFileIdentifier, sessionType, date):
        self.session = '_'.join([date, sessionID])
        self.behavFileIdentifier = behavFileIdentifier
        self.sessionType = sessionType
        self.plotType = ''
        self.report = ''

    def set_plot_type(self, plotTypeStr, report='main'):
        self.plotType = plotTypeStr
        self.report = report


class Cluster(object):

    def __init__(
            self,
            animalName,
            date,
            depth,
            tetrode,
            experimenter,
            paradigm,
            clusterNumber,
            ephysSessionList,
            behavFileList,
            sessionTypes,
            soundResponsive,
            laserPulseResponse,
            followsLaserTrain,
            comments=''):

        self.animalName = animalName
        self.date = date
        self.depth = depth
        self.tetrode = tetrode
        self.experimenter = experimenter
        self.paradigm = paradigm,
        self.cluster = clusterNumber
        self.tetrode = tetrode
        self.clusterNumber = clusterNumber
        self.ephysSessionList = ephysSessionList
        self.behavFileList = behavFileList
        self.sessionTypes = sessionTypes
        self.soundResponsive = soundResponsive
        self.laserPulseResponse = laserPulseResponse
        self.followsLaserTrain = followsLaserTrain
        self.comments = comments

        self.clusterID = '_'.join([animalName,
                                   date,
                                   str(depth),
                                   'TT{}'.format(self.tetrode),
                                   str(clusterNumber)])


class LoadedCluster(Cluster):

    def __init__(self, decodedDict):
        for key in decodedDict:
            if key not in [
                    '__class__',
                    '__module__']:  # FIXME: get rid of this, it does not seem useful
                setattr(self, key, decodedDict[key])


class JSONCellDB(object):

    def __init__(self, dbFilename):
        self.dbFilename = dbFilename
        clusterDB = self.connect(dbFilename)
        self.clusterList = self.build_clusters(clusterDB)
        self.clusterIDList = self.get_cluster_IDs(self.clusterList)

    def connect(self, dbFilename):
        if os.path.isfile(dbFilename):
            # This should open a new file if the file does not exist
            with open(dbFilename, 'r+') as f:
                clusterDB = json.load(f)
        else:  # No file to load - create it?
            clusterDB = []
        return clusterDB

    def build_clusters(self, clusterDB):
        loadedClusters = [LoadedCluster(d) for d in clusterDB]
        return loadedClusters

    def get_cluster_IDs(self, clusterList):
        clusterIDList = [
            c.clusterID.encode(
                'utf8',
                'ignore') for c in self.clusterList]
        return clusterIDList

    def add_clusters(self, clusterObjList):
        for clusterObj in clusterObjList:
            if clusterObj.clusterID not in self.clusterIDList:
                self.clusterList.append(clusterObj)
                self.clusterIDList = self.get_cluster_IDs(self.clusterList)
            else:
                print "Attempted to add duplicate cluster: {}".format(clusterObj.clusterID)

    def write_database(self):
        with open(self.dbFilename, 'w') as f:
            f.write('[\n')
            for indClust, clusterFile in enumerate(self.clusterList):
                f.write(
                    json.dumps(
                        clusterFile,
                        indent=4,
                        sort_keys=True,
                        default=convert_to_builtin_type))
                if indClust < len(self.clusterList) - 1:
                    f.write(',\n')
            f.write('\n]')
