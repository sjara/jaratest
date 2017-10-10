import pandas as pd
import band_ephys_analysis as ephysanalysis
import band_plots
reload(ephysanalysis)
reload(band_plots)

PV_CHR2_MICE = ['band004', 'band026', 'band032', 'band033']
SOM_CHR2_MICE = ['band005', 'band015', 'band016', 'band027', 'band028', 'band029', 'band030', 'band031', 'band034']
EXCLUDED_DATES = ['2017-07-27','2017-08-02']

CASE = 103

db = pd.read_hdf('/home/jarauser/src/jaratest/anna/analysis/all_clusters.h5','database',index_col=0)

if CASE==100:
    db = pd.read_hdf('/home/jarauser/src/jaratest/anna/analysis/temp_db.h5','database',index_col=0)
    bestCells = db.query("isiViolations<0.02 and clusterQuality>2")
    for indCell, cell in bestCells.iterrows():
        harmIndex, atBestFreq, bestFreq = ephysanalysis.best_index(cell, 'harmonics')
        if atBestFreq:
            band_plots.plot_harmonics_summary(cell, harmIndex=harmIndex)
        else:
            band_plots.plot_harmonics_summary(cell)
if CASE==101:
    bestCells = db.query("isiViolations<0.02 and clusterQuality>2.5 and tuningFitR2>0.5 and nBandSpikes>1000 and octavesFromBestFreq<0.5")
    print len(bestCells)
    for indCell, cell in bestCells.iterrows():
        band_plots.plot_freq_bandwidth_tuning(cell, bandIndex=int(cell['bestBandIndex']))
elif CASE==102:
    bestCells = db.query("isiViolations<0.02 and clusterQuality>2.5 and tuningFitR2>0.5 and nBandSpikes>1000 and octavesFromBestFreq<0.3 and laserResponse==1")
    bestCells = bestCells.loc[~bestCells['date'].isin(EXCLUDED_DATES)]
    print(bestCells.loc[bestCells['subject'].isin(PV_CHR2_MICE)])
        
elif CASE==103:
    cell = db.iloc[7011]
    band_plots.plot_bandwidth_report(cell, int(cell['bestBandIndex']))