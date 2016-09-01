from jaratoolbox import spikesorting
import os
from jaratoolbox import settings
import numpy as np
from matplotlib import pyplot as plt

#Need to set clusters, then align all spikes and plot the report
#May need to just copy the whole report generation code...


#TODO: Make the average calculate across all waves for the cluster
def plot_waveforms_average_all(waveforms,ntraces=40,fontsize=8):
    '''
    Plot waveforms given array of shape (nChannels,nSamplesPerSpike,nSpikes)

    The average waveform is over the randomly-selected spikes, and not all of the spikes.
    '''
    (nSpikes,nChannels,nSamplesPerSpike) = waveforms.shape
    spikesToPlot = np.random.randint(nSpikes,size=ntraces)
    #NOTE: We are now aligning all waveforms
    alignedWaveforms = spikesorting.align_waveforms(waveforms)
    print 'Calculating mean of all waveforms'
    meanWaveforms = np.mean(alignedWaveforms,axis=0)
    scalebarSize = abs(meanWaveforms.min())

    xRange = np.arange(nSamplesPerSpike)
    for indc in range(nChannels):
        newXrange = xRange+indc*(nSamplesPerSpike+2)
        #NOTE: Now spikesToPlot is used as an index here
        wavesToPlot = alignedWaveforms[spikesToPlot,indc,:].T
        plt.plot(newXrange,wavesToPlot,color='k',lw=0.4,clip_on=False)
        plt.hold(True)
        plt.plot(newXrange,meanWaveforms[indc,:],color='0.75',lw=1.5,clip_on=False)
    plt.plot(2*[-7],[0,-scalebarSize],color='0.5',lw=2)
    plt.text(-10,-scalebarSize/2,'{0:0.0f}uV'.format(np.round(scalebarSize)),
             ha='right',va='center',ma='center',fontsize=fontsize)
    plt.hold(False)
    plt.axis('off')

class ClusterReportAverageAllSpikes(spikesorting.ClusterReportFromData):

    def __init__(self,dataTT,outputDir=None,filename=None,showfig=True,figtitle='',nrows=12):
        super(ClusterReportAverageAllSpikes, self).__init__(dataTT, outputDir, filename, showfig, figtitle, nrows)

    def plot_report(self,showfig=False):
        print 'Plotting report...'
        #plt.figure(self.fig)
        self.fig = plt.gcf()
        self.fig.clf()
        self.fig.set_facecolor('w')
        nCols = 3
        nRows = self.nRows
        #for indc,clusterID in enumerate(self.clustersList[:3]):
        for indc,clusterID in enumerate(self.clustersList):
            #print('Preparing cluster %d'%clusterID)
            if (indc+1)>self.nRows:
                print 'WARNING! This cluster was ignore (more clusters than rows)'
                continue
            tsThisCluster = self.dataTT.timestamps[self.spikesEachCluster[indc,:]]
            wavesThisCluster = self.dataTT.samples[self.spikesEachCluster[indc,:],:,:]
            # -- Plot ISI histogram --
            plt.subplot(self.nRows,nCols,indc*nCols+1)
            spikesorting.plot_isi_loghist(tsThisCluster)
            if indc<(self.nClusters-1): #indc<2:#
                plt.xlabel('')
                plt.gca().set_xticklabels('')
            plt.ylabel('c%d'%clusterID,rotation=0,va='center',ha='center')
            # -- Plot events in time --
            plt.subplot(2*self.nRows,nCols,2*(indc*nCols)+6)
            spikesorting.plot_events_in_time(tsThisCluster)
            if indc<(self.nClusters-1): #indc<2:#
                plt.xlabel('')
                plt.gca().set_xticklabels('')
            # -- Plot projections --
            plt.subplot(2*self.nRows,nCols,2*(indc*nCols)+3)
            spikesorting.plot_projections(wavesThisCluster)
            # -- Plot waveforms --
            plt.subplot(self.nRows,nCols,indc*nCols+2)
            ##NOTE: This comes from above, re-defined in this file
            plot_waveforms_average_all(wavesThisCluster)
        #figTitle = self.get_title()
        plt.figtext(0.5,0.92, self.figTitle,ha='center',fontweight='bold',fontsize=10)
        if showfig:
            #plt.draw()
            plt.show()

class TetrodeToClusterNewReport(spikesorting.TetrodeToCluster):

    def __init__(self,animalName,ephysSession,tetrode,features=None):
        super(TetrodeToClusterNewReport, self).__init__(animalName, ephysSession, tetrode, features)

    def save_report(self, dirname='reports_clusters'):
        #NOTE: Redefine to use the cluster report from this file
        reportDir = os.path.join(settings.EPHYS_PATH,self.animalName,dirname)
        if self.dataTT is None:
            self.load_waveforms()
        self.dataTT.set_clusters(os.path.join(self.clustersDir,'Tetrode%d.clu.1'%self.tetrode))
        figTitle = self.dataDir+' (T%d)'%self.tetrode
        self.report = ClusterReportAverageAllSpikes(self.dataTT,outputDir=reportDir,
                                            filename=self.reportFileName,figtitle=figTitle,
                                            showfig=False)

if __name__=="__main__":

    from jaratest.nick.utils import transferutils as tf
    reload(tf)

    def make_new_reports(subject, sessions, tetrode, features=['peak', 'valleyFirstHalf']):
        for session in sessions:
            tf.rsync_session_data(subject, session, skipIfExists=True)
        clusterDirs = ['{}_kk'.format(session) for session in sessions]
        for clusterDir in clusterDirs:
            tf.rsync_session_data(subject, clusterDir, skipIfExists=True)

        for session in sessions:
            oneTT = TetrodeToClusterNewReport(subject,
                                            session,
                                            tetrode,
                                            features)

            oneTT.save_report(dirname='new_report_average_all')

    CASE=1
    #Test053 self sessions wanted by phoebe
    if CASE==0:
        subject = 'test053'
        sessions = ['2015-06-15_16-05-58', '2015-07-07_17-21-43', '2015-06-11_15-46-05']
        tetrode=1

        make_new_reports(subject, sessions, tetrode)

    elif CASE==1:
        subject = 'adap017'
        sessions = ['2016-04-27_15-50-12', '2016-04-29_18-06-54']
        tetrode=3

        make_new_reports(subject, sessions, tetrode)
