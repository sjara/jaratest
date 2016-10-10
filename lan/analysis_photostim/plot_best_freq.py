'''
Script to plot best frequencies of photostim sites.
Lan Guo 20161006
'''


def plot_best_freq_n_tuning_range_all_sites(siteList, tuningFilename):
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    tuningDf = pd.read_csv(tuningFilename)
    plot = tuningDf.plot(x='stim_hemi', y='most_responsive_freq',kind='scatter')
    for indr, tuningRange in enumerate(tuningDf['responsive_freqs']):
        if not tuningRange is np.nan:
            responsiveFreqs=tuningRange.split(',')
            if len(responsiveFreqs) == 2:
                plt.vlines(tuningDf['stim_hemi'][indr]+((np.random.random()-0.5)/5),*responsiveFreqs,color='grey',linewidth=1)
            elif len(responsiveFreqs) == 1:
                plt.plot(tuningDf['stim_hemi'][indr]+((np.random.random()-0.5)/5),responsiveFreqs,color='grey')
            
    plt.xlim(0.5,2.5)
    plt.xticks([1,2],['left-hemi','right-hemi'])
    plt.show()


def calculate_psycurve_by_cond_n_tuning(siteList, tuningFilename):
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    tuningDf = pd.read_csv(tuningFilename)
    
    # ndarrays for storing psycurves in 
    noLaser = np.zeros(0,dtype = float)
    lowTuningLaser = np.zeros(0,dtype = float)
    highTuningLaser = np.zeros(0,dtype = float)
    midTuningLaser = np.zeros(0,dtype = float)
    noTuningLaser = np.zeros(0,dtype = float)

    # Make a dictionary mapping for selecting which cat to add to:
    laserPsycurveByTuning = {'none':noTuningLaser, 
                             'low':lowTuningLaser,
                             'mid':midTuningLaser,
                             'high':highTuningLaser}

    for inds, site in enumerate(siteList):
        tuningThisSite = tuningDf.loc[(tuningDf['animalName']==site.animalName)&(tuningDf['session']==site.date)]
        if np.any(tuningThisSite): #this site in tuning database
            #freqs = percentRightwardDfThisSite['freqs']
            tuningFreqCat = tuningThisSite['response_to_curve'].values[0]
            #bestFreqThisSite = tuningThisSite['most_responsive_freq'].values
            # Calculate percent rightward choice for each freq separately for no_laser and laser conditions
            percentRightwardDfThisSite = site.calculate_percent_rightward_each_freq_each_cond()
            #pdb.set_trace()
            percentRightwardNoLaser = percentRightwardDfThisSite.ix[:,0].values
            percentRightwardLaser = percentRightwardDfThisSite.ix[:,1].values
            # Save calculated percent rightward choice based on whether best frequency this site is 'low', 'mid', or 'high' 
            if inds == 0:
                noLaser = percentRightwardNoLaser
            else:
                noLaser = np.vstack((noLaser,percentRightwardNoLaser))
            if not np.any(laserPsycurveByTuning[tuningFreqCat]):
                laserPsycurveByTuning[tuningFreqCat] = percentRightwardLaser
            else:
                laserPsycurveByTuning[tuningFreqCat] = np.vstack((laserPsycurveByTuning[tuningFreqCat],percentRightwardLaser))

                # Built ndarrays with rows being behav sessions and columns being frequencies in the psycurve
            
    # Return the ndarrays storing all psycurves rightward choice
    #pdb.set_trace()
    return (noLaser, laserPsycurveByTuning['low'], laserPsycurveByTuning['mid'], laserPsycurveByTuning['high'], laserPsycurveByTuning['none'])



def plot_psycurve_by_cond_n_tuning(siteList, tuningFilename, aggregateFunc='mean'):
    '''
    Take ndarrays containing psycurve for all tuning categories, plot aggregate psycurve based on the aggregate method given (can be either 'mean' or 'median').
    '''
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    (noLaser, lowTuningLaser, midTuningLaser, highTuningLaser, noTuningLaser) = calculate_psycurve_by_cond_n_tuning(siteList, tuningFilename) #ndarrays with rows being behav sessions and columns being frequencies in the psycurve
    dfToPlot = pd.DataFrame()
    if aggregateFunc == 'mean':
        #dfToPlot = pd.DataFrame(index = range(1,7))
        dfToPlot['no laser'] = np.mean(noLaser, axis=0)
        dfToPlot['laser_site tuned to low freqs'] = np.mean(lowTuningLaser, axis=0)
        dfToPlot['laser_site tuned to mid freqs'] = np.mean(midTuningLaser, axis=0)
        dfToPlot['laser_site tuned to high freqs'] = np.mean(highTuningLaser, axis=0)
        dfToPlot['laser_site with no tuning'] = np.mean(noTuningLaser, axis=0)
        #pdb.set_trace()
    elif aggregateFunc == 'median':
        dfToPlot['no laser'] = np.median(noLaser, axis=0)
        dfToPlot['laser_site tuned to low freqs'] = np.median(lowTuningLaser, axis=0)
        dfToPlot['laser_site tuned to mid freqs'] = np.median(midTuningLaser, axis=0)
        dfToPlot['laser_site tuned to high freqs'] = np.median(highTuningLaser, axis=0)
        dfToPlot['laser_site with no tuning'] = np.median(noTuningLaser, axis=0)
    
    plt.figure()
    dfToPlot.plot(linewidth=2)
    plt.title('Photostim {} psycurve by best freq'.format(aggregateFunc))
