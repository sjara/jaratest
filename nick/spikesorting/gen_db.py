
    def site_cluster_correlation(self, experiment, site, tetrode, cmap='jet'):
        #Has to load the waves for each cluster across all the sessions of the site
        ## Waves have to be aligned and flattened

        siteObj = self.inforec.experiments[experiment].sites[site]

        idString = 'exp{}site{}'.format(experiment, site)

        #Use cms to load all the waveforms
        oneTT = cms.MultipleSessionsToCluster(siteObj.subject,
                                              siteObj.session_ephys_dirs(),
                                              tetrode,
                                              idString)

        oneTT.load_all_waveforms()
        oneTT.set_clusters_from_file()

        # import ipdb; ipdb.set_trace()

        reportDir = 'multisession_{}'.format(idString)
        reportFn = '{}.png'.format(tetrode)
        reportFull = os.path.join(settings.EPHYS_PATH, siteObj.subject, reportDir, reportFn)

        reportImage = mpimg.imread(reportFull)

        plt.figure()
        plt.imshow(reportImage)
        plt.show()

        clustersPerTetrode = 12
        wavesize = 160

        allWaveforms = np.empty((clustersPerTetrode, wavesize))

        for indc in range(clustersPerTetrode):
            # print 'Estimating average waveform for {0} T{1}c{2}'.format(ephysSession,tetrode,indc+1)

            # DONE: get waveforms for one cluster
            #Add 1 to the cluster index because clusters start from 1
            waveforms = oneTT.samples[oneTT.clusters==indc+1, :, :]

            alignedWaveforms = spikesorting.align_waveforms(waveforms)
            meanWaveforms = np.mean(alignedWaveforms,axis=0)
            allWaveforms[indc,:] = meanWaveforms.flatten()


        ccSelf = clusteranalysis.row_corrcoeff(allWaveforms, allWaveforms)

        ccSelf = np.tril(ccSelf, k=-1)

        plt.figure()
        plt.imshow(ccSelf,clim=[0,1], cmap=cmap ,interpolation='nearest')
        plt.axis('image')
        plt.colorbar()
        plt.draw()

        return ccSelf
# Copied from cluster_inforec class for now
            #TODO: 
            if addToDB:
                for cluster in np.unique(oneTT.clusters):
                    clusterDict = {'tetrode':tetrode,
                                   'cluster':cluster}
                    clusterDict.update(siteObj.cluster_info())

                    clusterTimestamps = oneTT.timestamps[oneTT.clusters==cluster]

                    nspikes = len(clusterTimestamps)

                    ISI = np.diff(clusterTimestamps)
                    if len(ISI)==0:  # Hack in case there is only one spike
                        ISI = np.array(10)
                    isiViolations = np.mean(ISI<2e-3) # Assumes ISI in usec

                    clusterDict.update({'nspikes':nspikes,
                                        'isiViolations':isiViolations})

                    clusterDict.update({'experimentInd':experiment,
                                        'siteInd':site})

                    self.db = self.db.append(clusterDict, ignore_index=True)
