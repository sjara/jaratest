from jaratoolbox.test.nick.database import cellDB
reload(cellDB)

from jaratoolbox.test.nick.database import sitefuncs
reload(sitefuncs)
'''
2015-07-31 Nick Ponvert

This file constructs a cell database from several electrophysiology experiments, and
inclues examples for querying the database and manipulating the features of the clusters
in the database

'''


# ----------------------
##Defining standard session type strings for my experiment
# ----------------------

sessionTypes = {'nb':'noiseBurst',
                'lp':'laserPulse',
                'lt':'laserTrain',
                'tc':'tcHeatmap',
                'bf':'bestFreq',
                '3p':'3mWpulse',
                '1p':'1mWpulse'}

# ----------------------
##Adding an experiment, a site, and some sessions
# ----------------------

day1 = cellDB.Experiment(animalName = 'pinp003', date = '2015-06-24', experimenter = 'nick', defaultParadigm='laser_tuning_curve')

d1site1 = day1.add_site(depth = 3543, tetrodes = [6])
d1site1.add_session('15-22-29', None, sessionTypes['nb'])
d1site1.add_session('15-27-37', None, sessionTypes['lt'])
d1site1.add_session('15-31-48', 'a', sessionTypes['tc'])
d1site1.add_session('15-45-22', 'b', sessionTypes['bf'])

###Test of sitefunc for plotting the main report Lan and I use
#sitefuncs.nick_lan_daily_report(d1site1, 'site1', mainRasterInds=[0, 1, 3], mainTCind= 2)

#Choosing good clusters for this site
d1site1.add_clusters({6: [5, 8, 11]})

# ----------------------
##Adding a second experiment with another site
# ----------------------

day2 = cellDB.Experiment(animalName = 'pinp003', date = '2015-07-06', experimenter = 'nick', defaultParadigm='laser_tuning_curve')

d2site1 = day2.add_site(depth = 3509, tetrodes = [3, 6])

d2site1.add_session('11-15-56', None, sessionTypes['nb'])
d2site1.add_session('11-18-36', None, sessionTypes['lp'])
d2site1.add_session('11-21-26', None, sessionTypes['lt'])
d2site1.add_session('11-25-58', 'a', sessionTypes['tc'])
d2site1.add_session('11-39-46', None, sessionTypes['bf'])
d2site1.add_session('11-42-37', None, sessionTypes['3p'])
d2site1.add_session('11-45-22', None, sessionTypes['1p'])

d2site1.add_clusters({3: [2, 3, 5], 6:[3, 7]})

# ----------------------
##Initializing the database and adding clusters
# ----------------------

db = cellDB.CellDB()
db.add_clusters(d1site1.clusterList)
db.add_clusters(d2site1.clusterList)


# ----------------------
##Saving and loading databases
# ----------------------

#Writing currently overwrites the file. The proper way is to load the database,
#append new clusters to it, and then rewrite the file with the new contents added
#However, I am currently asking for confirmation unless you pass force=True.
dbfile = '/tmp/allcells.json'
db.write_to_json(dbfile)


db2 = cellDB.CellDB()
db2.load_from_json(dbfile)

# ----------------------
##Query functionality
# ----------------------

#Find a cell from a specific site
cell1 = db.find_cell_from_site('pinp003', '2015-06-24',  3543, 6, 5)


#Find a cell from a specific ephys session
cell2 = db.find_cell_from_session('pinp003', '2015-06-24_15-22-29', 6, 5)

#Intersectional query - find cells that satisfy certain conditions
#Will print the number of cells that satisfy the query unless you pass verbose=Flase
cellsWithStrongLaserSessions = db.query({
    'animalName': 'pinp003',
    'sessionTypes': '3mWpulse'
})

# ----------------------
##Setting Features
# ----------------------

#Setting features for all cells
db.set_features({'coolness': 'very cool'})

# Setting features for just cells with specific inds
db.set_features({'coolness': 'extra cool'}, [1, 3, 5])

#Setting features for all cells using an array the same length as the database
import numpy as np
featureArray = np.arange(len(db))
db.set_features_from_array('number', featureArray)


# ----------------------
##Querying Features
# ----------------------

#Features are a great idea but annoying to query with the regular query method.
#There are several methods that make querying features much easier and more powerful

#Feature queries
extraCoolCells = db.query_features({'coolness': 'extra cool'}, verbose=False)

#FIXME: This should return a boolean
#FIXME: Or just get the array of values for a particular feature - Then we could do all the calculations ourselves. 

#Feature queries with custom comparison functions
#This method takes a feature value and a comparison function, and uses the function to
#compare the supplied value to the value of each cell. You can either define your own
#comparison function and pass it, or import one and use it.


import operator #Standard library module with generic operator functions (gt (>), lt (<), etc.)
highNumberCells = db.query_features_custom_op({'number': 3}, operator.gt, verbose=False)
lowNumberCells = db.query_features_custom_op({'number': 3}, operator.lt, verbose=False)

# -----------------------
##Getting the data from a cluster to make a plot
# -----------------------

#Sessions with no behav data return just the ephys
cell1NoisePhys = cell1.get_data_filenames('noiseBurst')

#FIXME: Always return a tuple, even if there is no behav data - call this get_filenames
#Sessions with behav data return the tuple (ephysFilename, behavFilename)
cell1TuningPhys, cell1TuningBehavior = cell1.get_data_filenames('tcHeatmap')

#If you have a sessionTypes dict you can use that here as well
cell1LaserTrainPhys = cell1.get_data_filenames(sessionTypes['lt'])

# -----------------------
##Still to do (non critical)
# -----------------------
# Graceful failures - if you try to grab the data files and you give the wrong session types,
# it should warn you and tell you what session types are available to use
# There should be similar behavior for regular queries and feature queries
