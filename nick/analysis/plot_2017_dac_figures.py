import pandas
from jaratest.nick.database import dataloader_v3 as dataloader
from jaratoolbox import spikesanalysis
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import patches
from jaratoolbox import colorpalette
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis
from jaratest.nick.reports.pinp_report import get_colors
import os

dbFn = '/home/nick/data/database/corticostriatal_master_2017-06-01_13-00-07.h5'
db = pandas.read_hdf(dbFn, 'database')

dbStrFn = '/home/nick/data/database/corticostriatal_striatumcells_2017-05-30_13-27-08.h5'
dbStr = pandas.read_hdf(dbStrFn, 'database')

db = db.append(dbStr, ignore_index=True)

soundResponsive = db.query('isiViolations<0.02 and shapeQuality>2 and noisePval<0.05')
soundNoLaserResponsive = db.query('isiViolations<0.02 and shapeQuality>2 and noisePval<0.05 and (pulsePval>0.05 or trainRatio<0.8)')
soundLaserResponsive = db.query('isiViolations<0.02 and shapeQuality>2 and noisePval<0.05 and pulsePval<0.05 and trainRatio>0.8')

thalNoLaser = soundNoLaserResponsive.groupby('brainarea').get_group('rightThal')
thalLaser = soundLaserResponsive.groupby('brainarea').get_group('rightThal')
acNoLaser = soundNoLaserResponsive.groupby('brainarea').get_group('rightAC')
acLaser = soundLaserResponsive.groupby('brainarea').get_group('rightAC')
astr = soundResponsive.groupby('brainarea').get_group('rightAstr')

CASE=0
#Plotting highest AM sync rate
if CASE==0:
    from collections import Counter
    feature = 'highestSync'

    lowFreq = 4
    highFreq = 128
    nFreqs = 11
    freqs = np.logspace(np.log10(lowFreq),np.log10(highFreq),nFreqs)
    freqs = np.round(freqs, decimals=1)
    freqs = np.r_[0, freqs]

    tdataNL = np.round(thalNoLaser[feature][pandas.notnull(thalNoLaser[feature])], decimals=1)
    tdataL = np.round(thalLaser[feature][pandas.notnull(thalLaser[feature])], decimals=1)
    acdataNL = np.round(acNoLaser[feature][pandas.notnull(acNoLaser[feature])], decimals=1)
    acdataL = np.round(acLaser[feature][pandas.notnull(acLaser[feature])], decimals=1)
    astrdata = np.round(astr[feature][pandas.notnull(astr[feature])], decimals=1)

    tCountNL = Counter(tdataNL)
    tCountL = Counter(tdataL)
    acCountNL = Counter(acdataNL)
    acCountL = Counter(acdataL)
    astrCount = Counter(astrdata)

    tHeightsNL = [100*tCountNL[freq]/np.double(len(tdataNL)) for freq in freqs]
    tHeightsL = [100*tCountL[freq]/np.double(len(tdataL)) for freq in freqs]
    acHeightsNL = [100*acCountNL[freq]/np.double(len(acdataNL)) for freq in freqs]
    acHeightsL = [100*acCountL[freq]/np.double(len(acdataL)) for freq in freqs]
    astrHeights = [100*astrCount[freq]/np.double(len(astrdata)) for freq in freqs]

    index = np.arange(len(freqs))
    bar_width=0.35
    plt.clf()
    fig = plt.gcf()
    fig.set_size_inches(10.5, 3.7)
    linewidth=2
    fontsize=20

    plt.clf()

    ax = plt.subplot(211)
    rects11 = plt.bar(index,
                    tHeightsNL,
                    bar_width,
                    label='Thalamus',
                    facecolor='w',
                    edgecolor=colorpalette.TangoPalette['Chameleon3'],
                    linewidth = linewidth)
    plt.hold(1)
    rects12 = plt.bar(index+bar_width,
                    tHeightsL,
                    bar_width,
                    label='Thalamus',
                    facecolor=colorpalette.TangoPalette['Chameleon3'],
                    edgecolor=colorpalette.TangoPalette['Chameleon3'],
                    linewidth = linewidth)

    plt.xticks(index + bar_width, freqs)
    plt.yticks([0, 40])
    plt.xticks([])
    # plt.ylim([0, 35])
    extraplots.boxoff(ax)
    extraplots.set_ticks_fontsize(ax, fontsize)

    ax = plt.subplot(212)
    rects11 = plt.bar(index,
                    acHeightsNL,
                    bar_width,
                    label='AC',
                    facecolor='w',
                    edgecolor=colorpalette.TangoPalette['ScarletRed2'],
                    linewidth = linewidth)
    plt.hold(1)
    rects12 = plt.bar(index+bar_width,
                    acHeightsL,
                    bar_width,
                    label='AC',
                    facecolor=colorpalette.TangoPalette['ScarletRed2'],
                    edgecolor=colorpalette.TangoPalette['ScarletRed2'],
                    linewidth = linewidth)

    plt.xticks(index + bar_width, freqs)
    plt.ylim([0, 35])
    plt.yticks([0, 30])
    # plt.xticks([])
    ax.set_xticklabels(map(int, np.floor(freqs)))
    extraplots.boxoff(ax)
    extraplots.set_ticks_fontsize(ax, fontsize)

    # ax =  plt.subplot(313)
    # rects11 = plt.bar(index+0.5*bar_width,
    #                 astrHeights,
    #                 bar_width,
    #                 label='astr',
    #                 facecolor=colorpalette.TangoPalette['SkyBlue2'],
    #                 edgecolor=colorpalette.TangoPalette['SkyBlue2'],
    #                 linewidth = linewidth)

    # plt.xticks(index + bar_width, freqs)
    # plt.ylim([0, 35])
    # plt.yticks([0, 30])
    # extraplots.boxoff(ax)
    # extraplots.set_ticks_fontsize(ax, fontsize)

    fig = plt.gcf()
    fig.set_size_inches(12, 7)
    plt.show()
    # plt.savefig('/home/nick/Dropbox/oregon/terms/y3spring/dac/figs/am_bar_plot.svg')
    plt.savefig('/home/nick/Dropbox/oregon/terms/y3spring/dac/figs/am_bar_plot_nostr.svg')

    # plt.clf()
    # plt.hist(tdata, histtype='step', color='g', weights=np.zeros_like(tdata) + 1. / tdata.size)
    # plt.hold(1)
    # plt.hist(acdata, histtype='step', color='r', weights=np.zeros_like(acdata) + 1. / acdata.size)
    # plt.hist(astrdata, histtype='step', color='b', weights=np.zeros_like(astrdata) + 1. / astrdata.size)
    # plt.show()

elif CASE==1:
    tbw = (thal['upperFreq']-thal['lowerFreq'])/thal['cf']
    tbw = tbw[pandas.notnull(tbw)]

    acbw = (ac['upperFreq']-ac['lowerFreq'])/ac['cf']
    acbw = acbw[pandas.notnull(acbw)]

    astrbw = (astr['upperFreq']-astr['lowerFreq'])/astr['cf']
    astrbw = astrbw[pandas.notnull(astrbw)]

    plt.clf()
    plt.hist(tbw, histtype='step', color='g', weights=np.zeros_like(tbw) + 1. / tbw.size)
    plt.hold(1)
    plt.hist(acbw, histtype='step', color='r', weights=np.zeros_like(acbw) + 1. / acbw.size)
    plt.hist(astrbw, histtype='step', color='b', weights=np.zeros_like(astrbw) + 1. / astrbw.size)
    plt.show()

elif CASE==2:
    feature = 'threshold'

    tdata = thal[feature][pandas.notnull(thal[feature])]
    acdata = ac[feature][pandas.notnull(ac[feature])]
    astrdata = astr[feature][pandas.notnull(astr[feature])]

    plt.clf()
    plt.hist(tdata, histtype='step', color='g', weights=np.zeros_like(tdata) + 1. / tdata.size)
    plt.hold(1)
    plt.hist(acdata, histtype='step', color='r', weights=np.zeros_like(acdata) + 1. / acdata.size)
    plt.hist(astrdata, histtype='step', color='b', weights=np.zeros_like(astrdata) + 1. / astrdata.size)
    plt.show()

elif CASE==3:
    feature = 'amKWstat'

    tdata = thal[feature][pandas.notnull(thal[feature])]
    acdata = ac[feature][pandas.notnull(ac[feature])]
    astrdata = astr[feature][pandas.notnull(astr[feature])]

    plt.clf()
    plt.hist(tdata, histtype='step', color='g', weights=np.zeros_like(tdata) + 1. / tdata.size)
    plt.hold(1)
    plt.hist(acdata, histtype='step', color='r', weights=np.zeros_like(acdata) + 1. / acdata.size)
    plt.hist(astrdata, histtype='step', color='b', weights=np.zeros_like(astrdata) + 1. / astrdata.size)
    plt.show()

elif CASE==4:
    #Plotting some example TC Heatmaps

    plt.clf()
    ax5 = plt.subplot(111)


    #Thalamus
    # cell = db.query("subject=='pinp015' and date=='2017-02-15' and depth==2902 and tetrode==8 and cluster==6").iloc[0]
    # cell = db.query("subject=='pinp017' and date=='2017-03-28' and depth==3074 and tetrode==1 and cluster==5").iloc[0]
    # cell = db.query("subject=='pinp016' and date=='2017-03-14' and depth==3703 and tetrode==8 and cluster==4").iloc[0]

    #AC
    # cell = db.query("subject=='pinp017' and date=='2017-03-23' and depth==1518 and tetrode==4 and cluster==3").iloc[0]
    # cell = db.query("subject=='pinp016' and date=='2017-03-09' and depth==1904 and tetrode==6 and cluster==6").iloc[0]
    # cell = db.query("subject=='pinp017' and date=='2017-03-22' and depth==1143 and tetrode==4 and cluster==6").iloc[0]
    #ASTR
    cell = db.query("subject=='pinp020' and date=='2017-05-10' and depth==2682 and tetrode==7 and cluster==3").iloc[0]

    spikeData, eventData = dataloader.get_session_ephys(cell, 'tc')
    eventOnsetTimes = eventData.get_event_onset_times()
    bdata = dataloader.get_session_bdata(cell, 'tc')
    #NOTE: We need to make the behav trials and the events the same size before this will work.
    if len(eventOnsetTimes)>len(bdata['currentFreq']):
        eventOnsetTimes = eventOnsetTimes[:len(bdata['currentFreq'])]

    timeRange = [0, 0.2]
    (spikeTimesFromEventOnset,
    trialIndexForEachSpike,
    indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
                                                                eventOnsetTimes,
                                                                timeRange)
    intensityEachTrial = bdata['currentIntensity']
    possibleIntensity = np.unique(intensityEachTrial)
    freqEachTrial = bdata['currentFreq']
    possibleFreq = np.unique(freqEachTrial)
    trialsEachCond = behavioranalysis.find_trials_each_combination(intensityEachTrial,
                                                                possibleIntensity,
                                                                freqEachTrial,
                                                                possibleFreq)
    avgSpikesArray = spikesanalysis.avg_num_spikes_each_condition(trialsEachCond, indexLimitsEachTrial)

    #Flip so high intensity is on top
    avgSpikesArray = np.flipud(avgSpikesArray)
    cax = plt.imshow(avgSpikesArray, interpolation='none', cmap='Blues')
    cbar = plt.colorbar(cax, format='%.1f')

    fontsize=25

    cbar.ax.set_ylabel('Avg spikes in\n200msec after stim', fontsize = fontsize)
    extraplots.set_ticks_fontsize(cbar.ax, fontsize)
    cbar.set_ticks([0, np.max(avgSpikesArray.ravel())])
    plt.clim([0, np.max(avgSpikesArray.ravel())])

    freqTicks = np.logspace(np.log2(2000), np.log2(40000), 3, base=2)
    freqTickLocations = np.linspace(0, 15, 3)

    ax5.set_xticks(freqTickLocations)
    ax5.set_xticklabels(['{:.1f}'.format(freq/1000.) for freq in freqTicks])

    ax5.set_xlabel('Frequency, kHz', fontsize=fontsize)

    ax5.set_yticks([0, 11])
    ax5.set_yticklabels([70, 15])

    ax5.set_ylabel('Intensity\ndB (SPL)', fontsize=fontsize)
    extraplots.set_ticks_fontsize(ax5, fontsize)
    # plt.title('cf:{:.0f} thresh:{:.0f}\nlower:{:.0f} upper:{:.0f}'.format(cell['cf'], cell['threshold'], cell['lowerFreq'], cell['upperFreq']), fontsize=9)
    
    figDir = '/home/nick/Dropbox/oregon/terms/y3spring/dac/figs/'
    figName = '{}_{}_{}_TT{}c{}.png'.format(cell['subject'],
                                            cell['date'],
                                            int(cell['depth']),
                                            int(cell['tetrode']),
                                            int(cell['cluster']))
    # plt.rcParams['svg.image_noscale'] = False
    fig = plt.gcf()

    plt.savefig(os.path.join(figDir, figName))

    plt.show()


elif CASE==5:
    #Example am rasters

    fontsize=20

    plt.clf()

    #Thal
    # cell = db.query("subject=='pinp015' and date=='2017-02-15' and depth==2902 and tetrode==8 and cluster==6").iloc[0]
    # cell = db.query("subject=='pinp016' and date=='2017-03-14' and depth==3703 and tetrode==8 and cluster==4").iloc[0]
    # cell = db.query("subject=='pinp015' and date=='2017-02-15' and depth==2902 and tetrode==6 and cluster==3").iloc[0]

    #AC
    # cell = db.query("subject=='pinp017' and date=='2017-03-22' and depth==1143 and tetrode==4 and cluster==5").iloc[0]
    # cell = db.query("subject=='pinp017' and date=='2017-03-23' and depth==1281 and tetrode==7 and cluster==2").iloc[0]

    # cell = db.query("noisePval<0.5 and brainarea=='rightAC' and highestSync==64").iloc[24]

    #ASTR
    cell = db.query("subject=='pinp020' and date=='2017-05-10' and depth==2682 and tetrode==7 and cluster==3").iloc[0]


    PLOT=1

    spikeData, eventData = dataloader.get_session_ephys(cell, 'am')
    eventOnsetTimes = eventData.get_event_onset_times()
    # eventOnsetTimes = eventData.get_event_onset_times(eventChannel=5)
    # eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, 0.5)
    bdata = dataloader.get_session_bdata(cell, 'am')
    colors = get_colors(len(np.unique(bdata['currentFreq'])))

    plt.clf()

    ms = 4
    sortArray=bdata['currentFreq']
    labels = ['{:d}'.format(int(freq)) for freq in np.unique(bdata['currentFreq'])]
    trialsEachCond = behavioranalysis.find_trials_each_type(sortArray, np.unique(sortArray))
    timeRange = [-0.2, 0.7]
    (spikeTimesFromEventOnset,
    trialIndexForEachSpike,
    indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
                                                                    eventOnsetTimes,
                                                                    timeRange)
    (pRaster,
        hcond,
        zline) = extraplots.raster_plot(spikeTimesFromEventOnset,
                                        indexLimitsEachTrial,
                                        timeRange,
                                        trialsEachCond=trialsEachCond,
                                        labels=labels,
                                        colorEachCond=colors)

    plt.xticks([0, 0.5])
    plt.xlabel('Time from sound onset (s)', fontsize=fontsize)
    plt.ylabel('AM rate (Hz)', fontsize=fontsize)

    #Set the marker size for better viewing
    plt.setp(pRaster, ms=ms)
    ax = plt.gca()

    extraplots.set_ticks_fontsize(ax, fontsize)

    
    figDir = '/home/nick/Dropbox/oregon/terms/y3spring/dac/figs/'
    figName = '{}_{}_{}_TT{}c{}_AM.png'.format(cell['subject'],
                                            cell['date'],
                                            int(cell['depth']),
                                            int(cell['tetrode']),
                                            int(cell['cluster']))
    if PLOT:
        plt.savefig(os.path.join(figDir, figName))

    plt.show()






