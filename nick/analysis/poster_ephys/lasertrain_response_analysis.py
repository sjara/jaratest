from matplotlib import pyplot as plt
import pandas
import numpy as np
from jaratest.nick.database import dataloader_v2 as dataloader
from jaratest.nick.database import dataplotter
from jaratoolbox import colorpalette
from jaratest.nick.stats import eventresponse
from jaratoolbox import extraplots

thaldbfn = '/home/nick/src/jaratest/nick/analysis/poster_ephys/thalamusdb_q10.pickle'
cortdbfn = '/home/nick/src/jaratest/nick/analysis/poster_ephys/cortexdb_q10.pickle'
thaldb = pandas.read_pickle(thaldbfn)
cortdb = pandas.read_pickle(cortdbfn)



if __name__=="__main__":

    CASE=2
    if CASE==1:
        reliability = np.empty(len(database))


        for indcell, cell in database.iterrows():
            reliability[indcell] = eventresponse.response_reliability(cell, pulse=4)

        database['reliability'] = reliability

        laserPulseThresh = 2
        noiseBurstThresh = 2
        isiThresh = 4
        laserResponsive = (database['isiViolations']<isiThresh) & (database['noiseburstZ']>noiseBurstThresh) & (database['laserpulseZ']>laserPulseThresh)

        plt.clf()
        plt.hist(database['reliability'][laserResponsive].dropna())
        plt.show()


    elif CASE==2:
        # timeRange = [-0.2, 0.6]
        timeRange = [-0.2, 1.0]
        # laserResponsive = (database['laserpulseZ']>2) & (database['isiViolations']<2)
        # for indcell, cell in database[laserResponsive].iterrows():

        database = cortdb
        # database = thaldb
        #Short
        # indices = [1220, 1278]
        # indices = [1280]

        #Long
        # indices = [878] #best indirect example, thal
        # indices = [1019] # best direct example, thal

        indices = [197] #best indirect example (overall), cortex

        psthcolor = colorpalette.TangoPalette['SkyBlue3']

        for index in indices:
            cell = database.ix[index]

            loader = dataloader.DataLoader(cell['subject'])
            fig = plt.clf()
            rastertype = 'LaserTrain'
            try:
                sessiontypeIndex = cell['sessiontype'].index(rastertype)
            except ValueError: #The cell does not have this session type
                continue
            sessionEphys = cell['ephys'][sessiontypeIndex]
            rasterSpikes = loader.get_session_spikes(sessionEphys, int(cell['tetrode']), cluster=int(cell['cluster']))
            spikeTimestamps = rasterSpikes.timestamps
            rasterEvents = loader.get_session_events(sessionEphys)
            eventOnsetTimes = loader.get_event_onset_times(rasterEvents)

            axRaster = plt.subplot(2, 1, 1)
            dataplotter.plot_raster(spikeTimestamps, eventOnsetTimes, ms=4, fillWidth=0, timeRange=timeRange)
            axRaster.set_axis_off()
            axPsth = plt.subplot(2, 1, 2)
            dataplotter.plot_psth(spikeTimestamps, eventOnsetTimes, binsize=10, timeRange=timeRange, colorEachCond=[psthcolor], lw=3)
            axPsth.set_xticks([0, 0.8])
            plt.locator_params(axis='y', nbins=3, tight=False)
            extraplots.boxoff(axPsth)
            plt.subplots_adjust(hspace=0, bottom=0.2, top=0.9, left=0.15, right=0.95)

            fontsize=20

            extraplots.set_ticks_fontsize(axPsth, fontsize)
            axPsth.set_ylabel('Spikes/sec', fontsize=fontsize)
            axPsth.set_xlabel('Time from first laser pulse (sec)', fontsize=fontsize)


            plt.show()

            # print indcell

            # plt.waitforbuttonpress()
