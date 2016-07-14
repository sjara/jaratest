'''
2015-07-24 Nick Ponvert


### Goal ###
Beginnings of the electrophysiology recording database for Jaralab.

INPUTS:

    To get the data from the database:
    - Experimenter
    - Subject
    - Date
    - Site (a string) (Have a func to get these if you dont know them)
    - Tetrode
    - Cluster
    - Session Type (string) (Have a func to get these if you dont know them)

    To create the database
    - Experimenter (Will get rid of in the future)
    - Paradigm

OUTPUTS: Behavior and physiology for a cell (for a particular session)
- All the sessions that were recorded for a cell
- Behavior data
- Phys data (both the spikes and the events)
- Data filenames (one for behav, spikes, events, clusters)

### Todo Stuff ###
- What to do when sessions from the same site occur on different days?
- We need to be able to create a database of sites in addition to a database of clusters
We want to be able to run analyses on the multi unit data or recluster
- Replace animalName with subject
- Add paradigm and experimenter to database records
- If data doesn't exist loader.get_cluster_data() does not fail. Just gives empty data.
- Regarding use of str() and repr(). Maybe the default repr() should be to print every attribute.
- Make the cluster repr more informative, including the mem location
- CellDB should have an easy way to add a cluster (without creating all the other stuff).
-- We need to be able to make clusters without making Experiments, sites, etc.
- cluster.get_data_filenames with no arguments should return the list of all
-- This should probably be a dict with keys being the session type and values being a tuple of (ephysFn, behavFn)

### Order of Arguments ###
animalName, date, ephysSessionList, behavFileList, experimenter, paradigm,

### Refile ###
- We should be able to cluster just a single session and get clusters from it

### Done stuff ###
TESTED, DONT THINK SO- If we change the experimenter for an Experiment, will it change for all of
the clusters because they are all pointing at the same place in memory?
DONE -  Change tetrodes to just tetrodes
DONE - Change behavFileIdentifier to something like behavSuffix
DONE - Sessions need to know about the paradigm that was used
DONE (I think)- Repeated arguments should be in the same order ('animalName', etc)
DONE - Sessions need to hold the whole behavior file name, not just the suffix. We will still create them by specifying the suffix
DONE- the database will ultimately give us back strings for the filenames of the ephys and behavior session, also cluster objects.
DONE- Cluster may need to have methods for returning ephys and behav filenames


- For next time: how do we send an email with what clusters to plot and then plot them very easily?

Design Decisions:

Should experiment be an object if it just holds strings? It seems like we are not using the site list. However, if we want to add the clusters for all of the sites to a database at one time, it may be nice to have a list of all of the site objects

Advantage: We are exlicitly creating site objects if the experiment is just a dict of strings.

It is possible to have each cluster hold the info about all of the sessions or to have each session hold all of the clusters that come from that session. So far we have chosen to have each cluster hold the info about what sessions it comes from.

Pros:
- Makes sense to think about the database as being a list of clusters, because we usually want to interact with a single cluster and get the info from all of the ephys sessions related to it.

Cons:
- This may be more redundant than having a hierarchical organization

At one point we decided that the best thing to do would be to have the database store information in a hierarchical way that minimizes the redundancy, and then have methods to convert this hierarchy into a list of clusters (with some redundancy) when we want to interact with the data.



'''

import json
import operator
import os

class CellDB(list):

    def __init__(self):

        '''
        This list subclass acts as a container for stored cluster objects.
        Current Problems: If you index the list, it generates a regular list instead of a new version of this object.
        '''
        super(CellDB, self).__init__()


    def add_clusters(self, clusters):
        '''
        The safe way to append clusters. Will not add a cluster if it already exists in the database.

        Args:
            clusters (list of Cluster objects): A list containing all of the cluster objects to be added.
        '''

        for cluster in clusters:
            if cluster.clusterID not in self.get_cluster_ids():
                self.append(cluster)
            else:
                print "Attemted to add duplicate cluster {}".format(cluster.clusterID)

    def get_cluster_ids(self):

        '''
        Will return a list containing the cluster id for each cluster in the database
        '''

        return [c.clusterID for c in self]

    def query(self, lookup_dict, verbose=True):
        '''
        The lookup dict will be like this: {'animalName': 'test000', 'date': '2014-06-24'}
        You can also do: {'animalName': ['test000', 'test001']}
        We need to figure out what to do when looking for cells that have a 'BestFreq' session,
        when looking for cells with a particular ephys session, etc since these attributes are lists
        '''
        #Start with either the entire DB or some pre-defined subset of it.
        queryResults = self

        #Iterate through the values in the query dictionary, narrowing the results each time.
        for attrName, attrVal in lookup_dict.iteritems():
            passing_clusters_this_attr = []
            for clu in queryResults:
                #Get the value of the attribute for this cluster
                clusterAttrVal = getattr(clu, attrName)

                #Some attributes, like sessions, sessionTypes, and behavFileIDs,
                #are lists. We should check each entry
                if isinstance(clusterAttrVal, list):
                    #Now we need to handle things differently depending on whether
                    #the supplied attribute value in the query was a list of possible
                    #values or a single value

                    #Compare the list of cluster attribute vals to a list
                    if isinstance(attrVal, list):
                        #This should pass if they share any items
                        if set(clusterAttrVal) & set(attrVal):
                            passing_clusters_this_attr.append(clu)
                            pass
                    else:
                        #Test whether the supplied value is in the cluster attribute
                        if attrVal in clusterAttrVal:
                            passing_clusters_this_attr.append(clu)
                            pass
                #If the cluster attribute val is not a list
                else:
                    #Compare a single cluster attribute to a list of possibilities
                    if isinstance(attrVal, list):
                        if clusterAttrVal in attrVal:
                            passing_clusters_this_attr.append(clu)
                            pass
                    #Compare a single cluster attribute to a single value
                    else:
                        if clusterAttrVal==attrVal:
                            passing_clusters_this_attr.append(clu)
                            pass
            queryResults = passing_clusters_this_attr
        if verbose:
            print "{} clusters satisfying these conditions".format(len(queryResults))
        return queryResults

    def find_cell_from_site(self, animalName, date, depth, tetrode, cluster):
        '''
        This method will return only a single cell
        '''

        cell = self.query({'animalName': animalName,
                           'date': date,
                           'depth': depth,
                           'tetrode': tetrode,
                           'cluster': cluster}, verbose=False)
        if cell:
            return cell[0]
        else:
            print "No clusters found"

    def find_cell_from_session(self, animalName, ephysSession, tetrode, cluster):

        cell = self.query({
            'animalName': animalName,
            'ephysSessionList': ephysSession,
            'tetrode': tetrode,
            'cluster': cluster}, verbose=False)
        if cell:
            return cell[0]
        else:
            print "No clusters found"

    def query_features(self, features_dict, verbose=True):
        '''
        The features dictionary is annoying to query with the regular query function because you
        have to write a dictionary inside the query dict. This method will search the features attr only.
        This method will only work if features have ONE value. It is not yet implemented for features that
        contain lists of values.
        '''
        queryResults = self
        for featureName, featureVal in features_dict.iteritems():
            if isinstance(featureVal, list):
                queryResults = [c for c in queryResults if c.features[featureName] in featureVal]
            else:
                queryResults = [c for c in queryResults if c.features[featureName] == featureVal]
        if verbose:
            print "{} clusters satisfying these conditions".format(len(queryResults))
        return queryResults

    def query_features_custom_op(self, features_dict, op=operator.eq, verbose=True):
        '''

        DEPRECATED: We should simply get an array of feature values so that we can do any arbitrary
        calculation. This should be combined with a method for efficently getting certain indices
        from the database.

        This method allows you to query using a custom comparison opeartor, like operator.gt()
        The operator function must compare the feature val of a cluster with the val you supply and
        return True or False.

        This method only works if you supply a single value as a feature val.
        Other constraints apply depending on the choice of opeartor function. When using
        functions from the opeartor module, this will probably only work well with numeric features
        '''
        queryResults = self
        for featureName, featureVal in features_dict.iteritems():
                queryResults = [c for c in queryResults if op(c.features[featureName], featureVal)]
        if verbose:
            print "{} clusters satisfying these conditions".format(len(queryResults))
        return queryResults

    def set_features(self, featuresDict, indsToSet=[]):
        '''
        Do we ever want to specify a range of inds to this function?

        Args:
            featuresDict (dict): A dictionary of feature names and values (example: {"coolness": "extra cool"})
            indsToSet (list): The indices of clusters in the database for which to set the features.
        '''
        if not indsToSet:
            indsToSet = range(len(self))
        for featureName, featureVal in featuresDict.iteritems():
            for ind in indsToSet:
                self[ind].features[featureName]=featureVal

    def set_features_from_array(self, featureName, featureArray):
        '''
        The feature array has to be the same length as the database

        Args:
            featureName (str): The name of the feature to set
            featureArray (array): The value for this feature for each cluster in the database. Must be the same length as the database
        '''
        if len(featureArray)!=len(self):
            print "The feature array has to be the same length as the database"
            pass
        for indClust, featureVal in enumerate(featureArray):
            self[indClust].features[featureName]=featureVal

    def write_to_json(self, filename, force=False):
        '''CAUTION: This will currently overwrite the json file. You should always load the most current
        database work with it, and then write the updated version when you are done.

        Args:
            filename (str): The path to the json file
            force (bool): Whether or not to proceed with overwriting the database file without asking for confirmation
        '''

        confirmation=''
        if not force:
            confirmation = raw_input("This will overwrite the .json file. Proceed? [yes/no] ")
        if (confirmation=='yes' or force):
            with open(filename, 'w') as f:
                f.write('[\n')
                for indClust, cluster in enumerate(self):
                    f.write(
                        json.dumps(
                            cluster.__dict__,
                            indent=4,
                            sort_keys=True))
                    if indClust < len(self) - 1:
                        f.write(',\n')
                f.write('\n]')
        elif confirmation=='no':
            print "Aborting"
        else:
            print "Please enter 'yes' or 'no'"

    def load_from_json(self, filename):

        '''
        Load clusters from a json file

        Args:
            filename (str): The path to the json file
        '''
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                jsonDict = json.load(f)
            self.add_clusters([LoadedCluster(d) for d in jsonDict])
        else:
            print "No database file found"

    def __str__(self):
        objStrs=[]
        for ind, cluster in enumerate(self):
            objStrs.append('Cell {}\nID: {}\nComments: {}\n\n'.format(ind, cluster.clusterID, cluster.comments))
        return ''.join(objStrs)

class Experiment(object):
    '''
    Experiment is a container of Sites.
    '''


    def __init__(self, animalName, date, experimenter, defaultParadigm=''):
        self.animalName = animalName
        self.date = date
        self.experimenter = experimenter
        self.defaultParadigm = defaultParadigm
        self.siteList = []
    def add_site(self, depth, tetrodes):

        '''
        Args:

        depth (int): The depth of the site in microns
        tetrodes (list): A list of the tetrode numbers that have good signals
        '''

        site = Site(animalName=self.animalName,
                    date=self.date,
                    experimenter=self.experimenter,
                    defaultParadigm=self.defaultParadigm,
                    tetrodes=tetrodes,
                    depth=depth)

        self.siteList.append(site)
        return site

    def __repr__(self):
        objStrings = []
        for key,value in sorted(vars(self).iteritems()):
            objStrings.append('%s: %s\n'%(key,str(value)))
        return ''.join(objStrings)
    def __str__(self):
        objStr = '{0} recording on {1} by {2}'.format(self.animalName,
                                                      self.date,
                                                      self.experimenter)
        return objStr


class Site(object):

    '''
    Class for holding information about a recording site.

    Will act as a parent for all of the Session objects that hold
    information about each individual recording session.
    '''

    def __init__(self, animalName, date, experimenter, defaultParadigm, tetrodes, depth=0):

        '''
        Args:

        depth (int): The site depth in microns
        tetrodes (list): A list of the tetrodes with good signals for this site
        '''

        self.depth = depth
        self.tetrodes = tetrodes
        self.animalName = animalName #Provided by Experiment
        self.date = date #Provided by Experiment
        self.experimenter = experimenter #Provided by Experiment
        self.defaultParadigm = defaultParadigm #Provided by Experiment
        self.sessionList = []
        self.clusterList = []

    def add_session(self, session, behavFileSuffix, sessionType, paradigm=None):
        '''
        Args:
            session (str): The timestamp for the ephys file (e.g. '11-22-33')
            behavFileSuffix (str): The suffix on the behavior file
            sessionType (str): An arbitrary string describing the session. Useful if standardized for a particular experiment (e.g. 'NoiseBurst')
            paradigm (str): The name of the paradigm that was used to collect the session. Defaults to the default paradigm for this site.
        '''

        if not paradigm:
            paradigm = self.defaultParadigm

        if behavFileSuffix:
            # if len(behavFileSuffix)==1: #This is just the suffix - need to add the date
            datestr = ''.join(self.date.split('-'))
            behavFileNameBaseName = '_'.join([self.animalName, paradigm, datestr])
            fullBehavFileName = '{}{}.h5'.format(behavFileNameBaseName, behavFileSuffix)
            # elif len(behavFileSuffix)==9: #Has the date but no paradigm - add the rest ##EDIT: I dont think we need this any more
            #     behavFileNameBaseName = '_'.join([self.animalName, paradigm])
            #     fullBehavFileName = '{}_{}.h5'.format(behavFileNameBaseName, behavFileSuffix)
        else:
            fullBehavFileName=None

        #If we need to record past midnight, just include the date in the session timestamp
        if len(session.split('_'))==2: #Has the date already
            ephysSession = session

        elif len(session.split('_'))==1: #Does not have the date already, assume to be the stored date
            ephysSession = '_'.join([self.date, session])


        session = Session(ephysSession, fullBehavFileName, sessionType)
        self.sessionList.append(session)
        return session

    def add_cluster(self,
                    tetrode,
                    cluster,
                    **kwargs):

        cluster = Cluster(
            animalName=self.animalName,
            date=self.date,
            depth=self.depth,
            tetrode=tetrode,
            cluster=cluster,
            ephysSessionList=self.get_session_ephys_filenames(),
            behavFileList=self.get_session_behav_filenames(),
            sessionTypes=self.get_session_types(),
            **kwargs)

        self.clusterList.append(cluster)
        return cluster

    def add_clusters(self, clusterDict):
        '''
        Add clusters from many tetrodes at once by passing a dictionary.

        Args:
            clusterDict (dict): A dictionary in the form: {tetrodeNumber: [clusterNumbers]}
        '''
        for tetrode, clusters in clusterDict.iteritems():
            for cluster in clusters:
                self.add_cluster(tetrode, cluster)


    def get_session_ephys_filenames(self):
        '''
        Returns a list of the ephys filenames for each session in the sessionList
        '''
        return [s.ephysFilename for s in self.sessionList]

    def get_mouse_relative_ephys_filenames(self):
        return [os.path.join(self.animalName, fn) for fn in self.get_session_ephys_filenames()]

    def get_session_behav_filenames(self):
        '''
        Returns a list of the behavior filenames for each session in the sessionList
        '''
        return [s.behavFilename for s in self.sessionList]

    def get_mouse_relative_behav_filenames(self):
        behavFns = self.get_session_behav_filenames()
        fnList = []
        for fn in behavFns:
            if fn:
                fnList.append(os.path.join(self.animalName, fn))
            else:
                fnList.append(None)

        return fnList

    def get_session_types(self):
        '''
        Returns a list of the session types for each session in the sessionList
        '''
        return [s.sessionType for s in self.sessionList]

    def __repr__(self):
        return "Site at {}um".format(self.depth)

    def __str__(self):
        return "Site at {}um".format(self.depth)

class Session(object):

    '''
    Class to hold information about a single session.
    '''

    def __init__(self, fullSessionFilename, fullBehavFilename, sessionType):
        self.ephysFilename = fullSessionFilename
        self.behavFilename = fullBehavFilename
        self.sessionType = sessionType

    def __repr__(self):
        return "{0} - {1}".format(self.ephysFilename, self.sessionType)

    def __str__(self):
        return "{0} - {1}".format(self.session, self.sessionType)


class Cluster(object):
    '''
    The init method currently sets the features attr to a copy of the features argument
    If we dont do this, all clusters will point to the same dictionary and we dont know why
    '''

    def __init__(
            self,
            animalName,
            date,
            depth,
            tetrode,
            cluster,
            ephysSessionList,
            behavFileList,
            sessionTypes,
            features={},
            comments=''):

        self.animalName = animalName
        self.date = date
        self.depth = depth
        self.tetrode = tetrode
        self.cluster = cluster
        self.ephysSessionList = ephysSessionList
        self.behavFileList = behavFileList
        self.sessionTypes = sessionTypes
        self.features = features.copy()
        self.comments = comments
        self.clusterID = '_'.join([animalName,
                                   date,
                                   str(depth),
                                   'TT{}'.format(self.tetrode),
                                   str(cluster)])

    def get_session_types(self):
        for ind, sessionType in enumerate(self.sessionTypes):
            print '{} - {}'.format(ind, sessionType)

    def get_data_filenames(self, sessionType=None, includeMouse=True):#TODO: Change mouse to subject
        '''
        Returns the ephys session folder name, or a tuple containing both the ephys filename
        and the behavior file name

        Args:
            sessionType (str): The string used to define the session when it was created
            includeMouse (bool): Whether to return the full filename joined to the mouse folder
        Returns:
            ephysFilename (str): The full name of the ephys session folder
            behavFilename (str): Also returned if the session has behavior data
        '''

        if sessionType:
            sessionIndex = self.sessionTypes.index(sessionType)
        else:
            print 'Cluster {} has the following sessions:\n'.format(self.clusterID)
            for ind, sessionType in enumerate(self.sessionTypes):
                print '{} - {}'.format(ind, sessionType)
            sessionIndex = raw_input("What session would you like? [index]: ")
            sessionIndex = int(sessionIndex)


        ephysFile = None
        behavFile = None

        #I think we will usually want to include the mouse directory in the output.
        #This will help when doing offline plotting of cells from many mice.
        #We will not have to have seperate DataLoader objects for each mouse that we deal with
        if includeMouse:
            ephysFile = os.path.join(self.animalName, self.ephysSessionList[sessionIndex])
            if self.behavFileList[sessionIndex]:
                behavFile = os.path.join(self.animalName, self.behavFileList[sessionIndex]) #We can't do the join if the behav file is None

        else:
            ephysFile = self.ephysSessionList[sessionIndex]
            behavFile = self.behavFileList[sessionIndex]

        return ephysFile, behavFile

    def __repr__(self): #TODO: Make this repr give more information about the object, including the mem location
        return self.clusterID

    def __str__(self):
        return self.clusterID

class LoadedCluster(Cluster):

    def __init__(self, decodedDict):
        for key in decodedDict:
            setattr(self, key, decodedDict[key])
