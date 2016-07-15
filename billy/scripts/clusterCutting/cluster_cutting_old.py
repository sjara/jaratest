import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
import itertools

import allcells_test055 as allcells
from jaratoolbox import loadbehavior
from jaratoolbox import settings
from jaratoolbox import ephyscore
import os
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots

class ClusterCutter(object):
    '''
    Nick Ponvert 05-10-2015
    
    GUI window for cutting a cluster. Accepts an N by M array of points, 
    where N is the number of spikes and M is the number of attributes 
    (i.e. peak amplitude on each wire). The window allows the user to click
    to define a set of points that are used to form a convex hull,
    and the cluster is cut using the hull. Multiple cuts can be performed in 
    any of the different dimensions. After cutting is complete, the 
    attribute self.inCluster will contain a boolean list which can be used to 
    select only the spikes that are in the cut cluster. 
    '''

    def __init__(self, animalName, ephysSession, tetrode, cluster):

        #find feature values
        self.animalName = animalName
        self.ephysSession = ephysSession
        self.tetrode = tetrode
        self.cluster = cluster
        self.featureNames = ['peak','valley','energy']
        self.dataDir = os.path.join(settings.EPHYS_PATH,self.animalName,self.ephysSession)
        self.tetrodeFile = os.path.join(self.dataDir,'Tetrode{0}.spikes'.format(self.tetrode))
        self.dataTT = None
        self.featureValues = None
        self.create_fet_files()
        self.points = self.featureValues[:,0:4]

        #Scatter the points
        #self.points = points

        #Figure out the dimensions of the data and how many combos there are 
        self.numDims=self.points.shape[1]
        self.combinations=[c for c in itertools.combinations(range(self.numDims), 2)]
        self.maxDim=len(self.combinations)-1

        #Start with the first combination
        self.dimNumber=0
        
        #All points start inside the cluster
        self.inCluster=np.ones(len(self.points), dtype=bool)
        self.outsideCluster=np.logical_not(self.inCluster)
        
        #Preserve the last cluster state for undo
        self.oldInsideCluster=self.inCluster
        self.oldOutsideCluster=self.outsideCluster
    
        #Make the fig and ax, and draw the initial plot
        self.fig=plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.draw_dimension(self.dimNumber)

        #Start the mouse handle.r and make an attribute to hold click pos
        self.mpid=self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.mouseClickData=[]

        #Start the key press handler
        self.kpid = self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

        #show the plot
        plt.show()

    def on_click(self, event):
        '''
        Method to record mouse clicks in the mouseClickData attribute
        and plot the points on the current axes
        '''
        
        self.mouseClickData.append([event.xdata, event.ydata])
        self.ax.plot(event.xdata, event.ydata, 'r+')
        self.fig.canvas.draw()

    
    def on_key_press(self, event):
        '''
        Method to listen for keypresses and take action
        '''
        
        #Function to cut the cluster
        if event.key=='c':
            #Only cut the cluster if there are 3 points or more
            if len(self.mouseClickData)>2:
                hullArray=np.array(self.mouseClickData)
                self.cut_cluster(self.points[:, self.combinations[self.dimNumber]], hullArray)
                self.draw_dimension(self.dimNumber)
                self.mouseClickData=[]
            else:
                pass
            
        #Function to undo the last cut
        if event.key=='u':
            self.mouseClickData=[]
            self.inCluster=self.oldInsideCluster
            self.outsideCluster=self.oldOutsideCluster
            self.draw_dimension(self.dimNumber)

        #Functions to cycle through the dimensions
        elif event.key=="<":
            if self.dimNumber>0:
                self.dimNumber-=1
            else:
                self.dimNumber=self.maxDim

            self.draw_dimension(self.dimNumber)
                

        elif event.key=='>':
            if self.dimNumber<self.maxDim:
                self.dimNumber+=1
            else:
                self.dimNumber=0

            self.draw_dimension(self.dimNumber)


    def draw_dimension(self, dimNumber):
        '''
        Method to draw the points on the axes using the current dimension number
        '''
    
        #Clear the plot and any saved mouse click data for the old dimension
        self.ax.cla()
        self.mouseClickData=[]
        
        #Find the point array indices for the dimensions to be plotted
        dim0 = self.combinations[self.dimNumber][0]
        dim1 = self.combinations[self.dimNumber][1]

        #Plot the points in the cluster in green, and points outside as light grey
        self.ax.plot(self.points[:,dim0][self.inCluster], self.points[:, dim1][self.inCluster], 'g.')
        self.ax.plot(self.points[:, dim0][self.outsideCluster], self.points[:,dim1][self.outsideCluster], marker='.', color='0.8', linestyle='None')

        #Label the axes and draw
        self.ax.set_xlabel('Dimension {}'.format(dim0))
        self.ax.set_ylabel('Dimension {}'.format(dim1))
        plt.title('press c to cut, u to undo last cut, < or > to switch dimensions')
        self.fig.canvas.draw()
        
    
    def cut_cluster(self, points, hull):
        ''' Method to take the current points from mouse input, 
        convert them to a convex hull, and then update the inCluster and 
        outsideCluster attributes based on the points that fall within 
        the hull'''

        #If the hull is not already a Delaunay instance, make it one
        if not isinstance(hull, Delaunay):
            hull=Delaunay(hull)

        #Save the old cluster for undo
        self.oldInsideCluster=self.inCluster
        self.oldOutsideCluster=self.outsideCluster

        #Find the ponts that are inside the hull
        inHull = hull.find_simplex(points)>=0

        #Only take the points that are inside the hull and the cluster
        #so we can cut from different angles and preserve old cuts
        newInsidePoints = self.inCluster & inHull
        self.inCluster = newInsidePoints
        self.outsideCluster = np.logical_not(self.inCluster)

    def load_waveforms(self):
        '''
        https://github.com/open-ephys/GUI/wiki/Data-format
        Since the samples are saved as unsigned integers, converting them to microvolts
        involves subtracting 32768, dividing by the gain, and multiplying by 1000.
        '''
        print 'Loading data...'
        self.dataTT = loadopenephys.DataSpikes(self.tetrodeFile)
        self.nSpikes = self.dataTT.nRecords# FIXME: this is specific to the OpenEphys format
        self.dataTT.samples = self.dataTT.samples.astype(float)-2**15# FIXME: this is specific to OpenEphys
        # FIXME: This assumes the gain is the same for all channels and records
        self.dataTT.samples = (1000.0/self.dataTT.gain[0,0]) * self.dataTT.samples
        self.dataTT.timestamps = self.dataTT.timestamps/self.dataTT.samplingRate

    def create_fet_files(self):
        '''
        # -- Create output directory --
        if not os.path.exists(self.clustersDir):
            print 'Creating clusters directory: %s'%(self.clustersDir)
            os.makedirs(self.clustersDir)
        if self.dataTT is None:
        '''
        self.load_waveforms()
        self.featureValues = self.calculate_features(self.dataTT.samples,self.featureNames)
        #write_fet_file(self.fetFilename,self.featureValues)

    def calculate_features(self,waveforms,featureNames):
        '''
        Parameters:
          waveforms: [nSpikes,nChannels,nSamples]
          featureNames: list of strings: 'peak','valley','energy'

        Returns:
          featureValues: [nSpikes, nFeatures*NChannels]
        '''
        nFeatures = len(featureNames)
        [nSpikes,nChannels,nSamples] = waveforms.shape
        featureValues = np.empty((nSpikes,0),dtype=float)
        for oneFeature in featureNames:
            print 'Calculating {0} ...'.format(oneFeature)
            if oneFeature=='peak':
                theseValues = waveforms.max(axis=2)
                featureValues = np.hstack((featureValues,theseValues))
            elif oneFeature=='valley':
                theseValues = waveforms.min(axis=2)
                featureValues = np.hstack((featureValues,theseValues))
            if oneFeature=='energy':
                theseValues = np.sqrt(np.sum(waveforms.astype(float)**2,axis=2))
                featureValues = np.hstack((featureValues,theseValues))
        return featureValues


            

if __name__=='__main__':
    '''
    mean=[1, 1, 1, 1]
    cov=np.random.random([4, 4])
    data = np.random.multivariate_normal(mean, cov, 1000)
    cw = ClusterCutter(data)
    '''
    SAMPLING_RATE=30000.0

    outputDir = '/home/billywalker/Pictures/raster_hist/'
    soundTriggerChannel = 0 # channel 0 is the sound presentation, 1 is the trial
    binWidth = 0.010 # Size of each bin in histogram in seconds

    timeRange = [-0.3,0.7] # In seconds. Time range for rastor plot to plot spikes (around some event onset as 0)

    ephysRootDir = settings.EPHYS_PATH

    experimenter = 'santiago'
    paradigm = '2afc'

    numOfCells = len(allcells.cellDB) #number of cells that were clustered on all sessions clustered
    subject = ''
    behavSession = ''
    ephysSession = ''

    for cellID in range(0,numOfCells):
        oneCell = allcells.cellDB[cellID]
        if (behavSession != oneCell.behavSession):


            subject = oneCell.animalName
            behavSession = oneCell.behavSession
            ephysSession = oneCell.ephysSession
            ephysRoot = os.path.join(ephysRootDir,subject)

            

            # -- Load Behavior Data --
            behaviorFilename = loadbehavior.path_to_behavior_data(subject,experimenter,paradigm,behavSession)
            bdata = loadbehavior.BehaviorData(behaviorFilename)
            numberOfTrials = len(bdata['choice'])

            # -- Load event data and convert event timestamps to ms --
            ephysDir = os.path.join(ephysRoot, ephysSession)
            eventFilename=os.path.join(ephysDir, 'all_channels.events')
            events = loadopenephys.Events(eventFilename) # Load events data
            eventTimes=np.array(events.timestamps)/SAMPLING_RATE #get array of timestamps for each event and convert to seconds by dividing by sampling rate (Hz). matches with eventID and 

            soundOnsetEvents = (events.eventID==1) & (events.eventChannel==soundTriggerChannel)


            eventOnsetTimes = eventTimes[soundOnsetEvents]

            rightward = bdata['choice']==bdata.labels['choice']['right']
            leftward = bdata['choice']==bdata.labels['choice']['left']
            invalid = bdata['outcome']==bdata.labels['outcome']['invalid']

            possibleFreq = np.unique(bdata['targetFrequency'])
            numberOfFrequencies = len(possibleFreq)


        tetrode = oneCell.tetrode
        cluster = oneCell.cluster
        clusterObj = ClusterCutter(subject, ephysSession, tetrode, cluster)
        #data = clusterObj.featureValues[:,0:4]
        #cw = ClusterCutter(data)
        raw_input("Press Enter to continue...")


        '''
        # -- Load Spike Data From Certain Cluster --
        spkData = ephyscore.CellData(oneCell)
        spkTimeStamps = spkData.spikes.timestamps

        (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
            spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimes,timeRange)

        #extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,fillWidth=None,labels=None)
        '''









 

