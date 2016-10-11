'''
Script to plot best frequencies of photostim sites.
Lan Guo 20161006
'''


def plot_best_freq_n_tuning_range_all_sites(siteList, tuningFilename):
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    tuningDf = pd.read_csv(tuningFilename)
    #plot = tuningDf.plot(x='stim_hemi', y='most_responsive_freq',kind='scatter')
    for indr, tuningRange in enumerate(tuningDf['responsive_freqs']):
        if not tuningRange is np.nan:
            responsiveFreqs=tuningRange.split(',')
            x = tuningDf['stim_hemi'][indr]+((np.random.random()-0.5)/5)
            if len(responsiveFreqs) == 2:
                plt.vlines(x,*responsiveFreqs,color='grey',linewidth=1)
            plt.plot(x,tuningDf['most_responsive_freq'][indr],'bo')
            
    plt.xlim(0.5,2.5)
    plt.xticks([1,2],['left-hemi','right-hemi'])
    plt.ylabel('Frequency (kHz)')
    plt.show()


def calculate_psycurve_by_tuning_by_stimhemi(siteList, tuningFilename):
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    tuningDf = pd.read_csv(tuningFilename)
    
    # ndarrays for storing psycurves in 
    noLaserLeft = np.zeros(0,dtype = float)
    noLaserRight = np.zeros(0,dtype = float)
    lowTuningLaser = np.zeros(0,dtype = float)
    highTuningLaser = np.zeros(0,dtype = float)
    midTuningLaser = np.zeros(0,dtype = float)
    noTuningLaser = np.zeros(0,dtype = float)

    # Make a dictionary mapping for selecting which cat to add to:
    laserPsycurveByTuningLeft = {'none':noTuningLaser, 
                                 'low':lowTuningLaser,
                                 'mid':midTuningLaser,
                                 'high':highTuningLaser}
    laserPsycurveByTuningRight = {'none':noTuningLaser, 
                                 'low':lowTuningLaser,
                                 'mid':midTuningLaser,
                                 'high':highTuningLaser}

    for inds, site in enumerate(siteList):
        tuningThisSite = tuningDf.loc[(tuningDf['animalName']==site.animalName)&(tuningDf['session']==site.date)]
        if np.any(tuningThisSite): #this site in tuning database
            #freqs = percentRightwardDfThisSite['freqs']
            stimHemi = tuningThisSite['stim_hemi'].values[0]
            tuningFreqCat = tuningThisSite['response_to_curve'].values[0]
            #bestFreqThisSite = tuningThisSite['most_responsive_freq'].values
            # Calculate percent rightward choice for each freq separately for no_laser and laser conditions
            percentRightwardDfThisSite = site.calculate_percent_rightward_each_freq_each_cond()
            #pdb.set_trace()
            percentRightwardNoLaser = percentRightwardDfThisSite.ix[:,0].values
            percentRightwardLaser = percentRightwardDfThisSite.ix[:,1].values
            # Save calculated percent rightward choice based on whether best frequency this site is 'low', 'mid', or 'high' 
            if stimHemi == 1: #Left hemi stim sessions
                if not np.any(noLaserLeft):
                    noLaserLeft = percentRightwardNoLaser
                else:
                    noLaserLeft = np.vstack((noLaserLeft,percentRightwardNoLaser))
                if not np.any(laserPsycurveByTuningLeft[tuningFreqCat]):
                    laserPsycurveByTuningLeft[tuningFreqCat] = percentRightwardLaser
                else:
                    laserPsycurveByTuningLeft[tuningFreqCat] = np.vstack((laserPsycurveByTuningLeft[tuningFreqCat],percentRightwardLaser))
            elif stimHemi == 2: #Right hemi stim sessions
                if not np.any(noLaserRight):
                    noLaserRight = percentRightwardNoLaser
                else:
                    noLaserRight = np.vstack((noLaserRight,percentRightwardNoLaser))
                if not np.any(laserPsycurveByTuningRight[tuningFreqCat]):
                    laserPsycurveByTuningRight[tuningFreqCat] = percentRightwardLaser
                else:
                    laserPsycurveByTuningRight[tuningFreqCat] = np.vstack((laserPsycurveByTuningRight[tuningFreqCat],percentRightwardLaser))
                # Built ndarrays with rows being behav sessions and columns being frequencies in the psycurve
            
    # Return the ndarrays or dictionaries storing all psycurves rightward choice for each stim hemisphere
    #pdb.set_trace()
    return (noLaserLeft, noLaserRight, laserPsycurveByTuningLeft, laserPsycurveByTuningRight)



def plot_psycurve_by_cond_n_tuning(siteList, tuningFilename, aggregateFunc='mean', byHemi=False):
    '''
    Take siteList and tuningFilename, calculate psycurve for all tuning categories for both stim hemisphere. Plot aggregate psycurve based on the aggregate method given (can be either 'mean' or 'median'). Can generate plots by hemisphere or for both hemis.
    '''
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    (noLaserLeft, noLaserRight, laserPsycurveByTuningLeft, laserPsycurveByTuningRight) = calculate_psycurve_by_tuning_by_stimhemi(siteList, tuningFilename)
    
    if byHemi: # Plot each stim hemi separately
        dfToPlotLeft = pd.DataFrame()
        dfToPlotRight = pd.DataFrame()
        if aggregateFunc == 'mean':
            dfToPlotLeft['noLaser'] = np.mean(noLaserLeft, axis=0)
            dfToPlotRight['noLaser'] = np.mean(noLaserRight, axis=0)
            dfToPlotLeft['laser_site tuned to low freqs'] = np.mean(laserPsycurveByTuningLeft['low'], axis=0)
            dfToPlotRight['laser_site tuned to low freqs'] = np.mean(laserPsycurveByTuningRight['low'], axis=0)
            dfToPlotLeft['laser_site tuned to mid freqs'] = np.mean(laserPsycurveByTuningLeft['mid'], axis=0)
            dfToPlotRight['laser_site tuned to mid freqs'] = np.mean(laserPsycurveByTuningRight['mid'], axis=0)
            dfToPlotLeft['laser_site tuned to high freqs'] = np.mean(laserPsycurveByTuningLeft['high'], axis=0)
            dfToPlotRight['laser_site tuned to high freqs'] = np.mean(laserPsycurveByTuningRight['high'], axis=0)
            dfToPlotLeft['laser_site with no tuning'] = np.mean(laserPsycurveByTuningLeft['none'], axis=0)
            dfToPlotRight['laser_site with no tuning'] = np.mean(laserPsycurveByTuningRight['none'], axis=0)
        elif aggregateFunc == 'median':
            dfToPlotLeft['noLaser'] = np.median(noLaserLeft, axis=0)
            dfToPlotRight['noLaser'] = np.median(noLaserRight, axis=0)
            dfToPlotLeft['laser_site tuned to low freqs'] = np.median(laserPsycurveByTuningLeft['low'], axis=0)
            dfToPlotRight['laser_site tuned to low freqs'] = np.median(laserPsycurveByTuningRight['low'], axis=0)
            dfToPlotLeft['laser_site tuned to mid freqs'] = np.median(laserPsycurveByTuningLeft['mid'], axis=0)
            dfToPlotRight['laser_site tuned to mid freqs'] = np.median(laserPsycurveByTuningRight['mid'], axis=0)
            dfToPlotLeft['laser_site tuned to high freqs'] = np.median(laserPsycurveByTuningLeft['high'], axis=0)
            dfToPlotRight['laser_site tuned to high freqs'] = np.median(laserPsycurveByTuningRight['high'], axis=0)
            dfToPlotLeft['laser_site with no tuning'] = np.median(laserPsycurveByTuningLeft['none'], axis=0)
            dfToPlotRight['laser_site with no tuning'] = np.median(laserPsycurveByTuningRight['none'], axis=0)
        plt.figure()
        dfToPlotLeft.plot(linewidth=2)
        plt.title('Left hemisphere photostim {} psycurve by best freq'.format(aggregateFunc))  
        plt.figure()
        dfToPlotRight.plot(linewidth=2)
        plt.title('Right hemisphere photostim {} psycurve by best freq'.format(aggregateFunc))  

    else: # Plot both hemi together
        dfToPlot = pd.DataFrame()
        if aggregateFunc == 'mean':
            dfToPlot['no laser'] = np.mean(np.vstack((noLaserLeft, noLaserRight)), axis=0)
            dfToPlot['laser_site tuned to low freqs'] = np.mean(np.vstack((laserPsycurveByTuningLeft['low'],laserPsycurveByTuningRight['low'])), axis=0)
            dfToPlot['laser_site tuned to mid freqs'] = np.mean(np.vstack((laserPsycurveByTuningLeft['mid'],laserPsycurveByTuningRight['mid'])), axis=0)
            dfToPlot['laser_site tuned to high freqs'] = np.mean(np.vstack((laserPsycurveByTuningLeft['high'],laserPsycurveByTuningRight['high'])), axis=0)
            dfToPlot['laser_site with no tuning'] = np.mean(np.vstack((laserPsycurveByTuningLeft['none'],laserPsycurveByTuningRight['none'])), axis=0)
            #pdb.set_trace()
        elif aggregateFunc == 'median':
            dfToPlot['no laser'] = np.mean(np.vstack((noLaserLeft, noLaserRight)), axis=0)
            dfToPlot['laser_site tuned to low freqs'] = np.mean(np.vstack((laserPsycurveByTuningLeft['low'],laserPsycurveByTuningRight['low'])), axis=0)
            dfToPlot['laser_site tuned to mid freqs'] = np.mean(np.vstack((laserPsycurveByTuningLeft['mid'],laserPsycurveByTuningRight['mid'])), axis=0)
            dfToPlot['laser_site tuned to high freqs'] = np.mean(np.vstack((laserPsycurveByTuningLeft['high'],laserPsycurveByTuningRight['high'])), axis=0)
            dfToPlot['laser_site with no tuning'] = np.mean(np.vstack((laserPsycurveByTuningLeft['none'],laserPsycurveByTuningRight['none'])), axis=0)

        plt.figure()
        dfToPlot.plot(linewidth=2)
        plt.title('Photostim {} psycurve by best freq'.format(aggregateFunc))
