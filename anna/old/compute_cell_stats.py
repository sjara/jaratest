import pandas as pd
import numpy as np
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import bandwidths_analysis_v2 as bandan
from jaratest.nick.database import dataloader_v2 as dataloader
import scipy.stats

reload(bandan)

def plot_scatter_with_histograms(xvals, yvals, colour='k', oneToOneLine=True, xlabel=None, ylabel=None, title=None):
    gs = gridspec.GridSpec(5, 5)
    xmin = np.floor(min(xvals))
    xmax = np.ceil(max(xvals))
    ymin = np.floor(min(yvals))
    ymax = np.ceil(max(yvals))
    plt.subplot(gs[1:, 0:4])
    plt.plot(xvals, yvals, 'o', color=colour)
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    if oneToOneLine:
        oneToOneMax = max([max(xvals),max(yvals)])
        plt.plot([0,oneToOneMax],[0,oneToOneMax],'b--')
    plt.xlim(xmin,xmax)
    plt.ylim(ymin,ymax)
    plt.subplot(gs[0, 0:4])
    plt.hist(xvals, np.linspace(xmin,xmax,50))
    plt.axis('off')
    plt.subplot(gs[1:,4])
    plt.hist(yvals, np.linspace(ymin,ymax,50), orientation='horizontal')
    plt.axis('off')
    if title is not None:
        plt.suptitle(title)
        
def plot_discrete_scatter_with_jitter(xvals, yvals, jitter=0.2, colour='k', xlabel=None, ylabel=None, title=None):
    xLabels = np.unique(xvals)
    yLabels = np.unique(yvals)
    xPlotVals = range(len(xLabels))
    yPlotVals = range(len(yLabels))
    xDict = dict(zip(xLabels,xPlotVals))
    yDict = dict(zip(yLabels,yPlotVals))
    newxvals = [xDict[i] for i in xvals]
    newyvals = [yDict[j] for j in yvals]
    if jitter > 0:
        newxvals = newxvals + (np.random.random_sample(len(newxvals))*2*jitter-jitter)
        newyvals = newyvals + (np.random.random_sample(len(newyvals))*2*jitter-jitter)
    plt.plot(newxvals,newyvals,'o',color=colour)
    ax = plt.gca()
    ax.set_xticks(xPlotVals)
    ax.set_yticks(yPlotVals)
    ax.set_xticklabels(xLabels)
    ax.set_yticklabels(yLabels)
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    if title is not None:
        plt.title(title)

'''Pass vals, list of lists or arrays containing values for each category'''        
def plot_categorical_scatter_with_mean(vals, categoryLabels, jitter=True, colours=None, xlabel=None, ylabel=None, title=None):
    import matplotlib.colors
    import scipy.stats
    import pdb
    numCategories = len(vals)
    plt.hold(True)
    if colours is None:
        colours = plt.cm.gist_rainbow(np.linspace(0,1,numCategories))
    for category in range(numCategories):
        edgeColour = matplotlib.colors.colorConverter.to_rgba(colours[category], alpha=0.5)
        xval = (category+1)*np.ones(len(vals[category]))
        if jitter:
            jitterAmt = np.random.random(len(xval))
            xval = xval + (0.3 * jitterAmt) - 0.15
        #pdb.set_trace()
        plt.plot(xval, vals[category], 'o', mec=edgeColour, mew = 4, mfc='none', ms=16)
        mean = np.mean(vals[category])
        sem = scipy.stats.sem(vals[category])
        print mean, sem
        plt.plot(category+1, mean, 'o', color='k', mec=colours[category], ms=20)
        plt.errorbar(category+1, mean, yerr = sem, color=colours[category])
    plt.xlim(0,numCategories+1)
    plt.ylim(0,1)
    ax = plt.gca()
    ax.set_xticks(range(1,numCategories+1))
    ax.set_xticklabels(categoryLabels, fontsize=16)
    if xlabel is not None:
        plt.xlabel(xlabel, fontsize=20)
    if ylabel is not None:
        plt.ylabel(ylabel, fontsize=20)
    if title is not None:
        plt.title(title)
    plt.show()
    
def sample_power_difftest(d, s, power=0.8, sig=0.05):
    z = scipy.stats.norm.isf([sig/2]) 
    zp = -1 * scipy.stats.norm.isf([power])
    n = (2*(s**2)) * ((zp + z)**2) / (d**2)
    return int(round(n[0]))

if __name__ == '__main__':
    CASE = 7
    
    if CASE==0:    
        db = pd.read_hdf('/home/jarauser/src/jaratest/anna/analysis/all_clusters.h5','database',index_col=0)
        #db = db[(db['clusterQuality']<3)]
        #db = db[(db['clusterQuality']>0)]
        db = db[(db['clusterQuality']==1)]
        db.to_hdf('/home/jarauser/src/jaratest/anna/analysis/good_cells_stats_v2.h5', 'database')
    elif CASE==1:
        db = pd.read_hdf('/home/jarauser/src/jaratest/anna/analysis/good_cells_stats_v2.csv','database',index_col=0)
        for indCell, cell in db.iterrows():
            bandan.plot_bandwidth_report_if_best(cell)
    elif CASE==3:
        db = pd.read_hdf('/home/jarauser/src/jaratest/anna/analysis/all_clusters.h5','database',index_col=0)
        atBestFreq = np.array(db['atBestFreq'].tolist())
        highSS = np.array(db['HighAmpSS'].tolist())
        lowSS = np.array(db['LowAmpSS'].tolist())
        contextCells = np.where(~np.isnan(lowSS))[0]
        contextLowSS = lowSS[contextCells]
        contextHighSS = highSS[contextCells]
        xlabel = 'Low Amplitude Suppression Score'
        ylabel = 'High Amplitude Suppression Score'
        plt.figure()
        plot_scatter_with_histograms(contextLowSS, contextHighSS, xlabel=xlabel, ylabel=ylabel, title='All cells')
        contextFreqs = atBestFreq[contextCells]
        bestCells = np.where(contextFreqs==1)[0]
        bestLowSS = contextLowSS[bestCells]
        bestHighSS = contextHighSS[bestCells]
        plt.figure()
        plot_scatter_with_histograms(bestLowSS, bestHighSS, colour='r', xlabel=xlabel, ylabel=ylabel, title='Cells at best frequency')
        highPeakSR = np.array(db['HighPeakSR'].tolist())[contextCells]
        lowPeakSR = np.array(db['LowPeakSR'].tolist())[contextCells]
        for i in range(len(lowPeakSR)):
            high = highPeakSR[i]
            low = lowPeakSR[i]
            if low>high:
                highPeakSR[i] = low
                lowPeakSR[i] = high
        plt.figure()
        xlabel = 'Low Peak Spike Rate'
        ylabel = 'High Peak Spike Rate'
        plot_scatter_with_histograms(lowPeakSR, highPeakSR, xlabel=xlabel, ylabel=ylabel, title='All cells')
        bestLowSR = lowPeakSR[bestCells]
        bestHighSR = highPeakSR[bestCells]
        plt.figure()
        plot_scatter_with_histograms(bestLowSR, bestHighSR, colour='r',xlabel=xlabel, ylabel=ylabel, title='Cells at best frequency')
        lowPeakLoc = np.array(db['LowPeakLoc'].tolist())[contextCells]
        highPeakLoc = np.array(db['HighPeakLoc'].tolist())[contextCells]
        plt.figure()
        xlabel = 'Low Amp Peak Location'
        ylabel = 'High Amp Peak Location'
        plot_discrete_scatter_with_jitter(lowPeakLoc, highPeakLoc, xlabel=xlabel, ylabel=ylabel, title='All cells')
        bestLowLoc = lowPeakLoc[bestCells]
        bestHighLoc = highPeakLoc[bestCells]
        plt.figure()
        plot_discrete_scatter_with_jitter(bestLowLoc, bestHighLoc, colour='r', xlabel=xlabel, ylabel=ylabel, title='Cells at best frequency')
    elif CASE==4:
        db = pd.read_hdf('/home/jarauser/src/jaratest/anna/analysis/all_clusters.h5','database',index_col=0)
        thalmice = db.query("subject=='band022' or subject=='band023'")
        thalCells = thalmice.query("isiViolations<0.02 and nSpikes>2000 and clusterQuality>2.5 and atBestFreq==1")
        thalcellSS = thalCells['HighAmpSS'].tolist()
        PVmice = db.query("subject=='band004' or subject=='band026'")
        PVCells = PVmice.query("laserResponse==1 and atBestFreq==1 and isiViolations<0.02 and clusterQuality>2.5")
        PVcellSS = PVCells['HighAmpSS'].tolist()
        SOMmice = db.query("subject=='band005' or subject=='band015' or subject=='band016' or subject=='band027' or subject=='band028' or subject=='band029' or subject=='band030' or subject=='band031'")
        SOMCells = SOMmice.query("isiViolations<0.02 and clusterQuality>2.5 and atBestFreq==1 and laserResponse==1 and nSpikes>2000")
        SOMcellSS = SOMCells['HighAmpSS'].tolist()
        notThalMice = db.query("subject!='band022' and subject!='band023'")
        otherCells = notThalMice.query("isiViolations<0.02 and clusterQuality>2.5 and atBestFreq==1 and laserResponse!=1 and nSpikes>2000")
        othercellSS = otherCells['HighAmpSS'].tolist()
        othercellSS = [x for x in othercellSS if (np.isnan(x) == False)]
        plot_categorical_scatter_with_mean([thalcellSS,PVcellSS,SOMcellSS,othercellSS], ['thalamus','AC-PV','AC-SOM','AC-unidentified'], colours = ['0.5','b','g','0.5'], xlabel='Cell type', ylabel='Suppression score', title='70dB Suppression')
    elif CASE==5:
        db = pd.read_hdf('/home/jarauser/src/jaratest/anna/analysis/all_clusters.h5','database',index_col=0)
        thalmice = db.query("subject=='band022' or subject=='band023'")
        thalCells = thalmice.query("isiViolations<0.02 and nSpikes>2000 and clusterQuality>2.5 and atBestFreq==1")
        thalcellSS = thalCells['LowAmpSS'].tolist()
        PVmice = db.query("subject=='band004' or subject=='band026'")
        PVCells = PVmice.query("laserResponse==1 and atBestFreq==1 and isiViolations<0.02 and clusterQuality>2.5 and nSpikes>2000")
        PVcellSS = PVCells['LowAmpSS'].tolist()
        SOMmice = db.query("subject=='band005' or subject=='band015' or subject=='band016' or subject=='band027' or subject=='band028' or subject=='band029' or subject=='band030' or subject=='band031'")
        SOMCells = SOMmice.query("isiViolations<0.02 and clusterQuality>2.5 and atBestFreq==1 and laserResponse==1 and nSpikes>2000")
        SOMcellSS = SOMCells['LowAmpSS'].tolist()
        SOMcellSS = [x for x in SOMcellSS if (np.isnan(x) == False)]
        notThalMice = db.query("subject!='band022' and subject!='band023'")
        otherCells = notThalMice.query("isiViolations<0.02 and clusterQuality>2.5 and atBestFreq==1 and laserResponse!=1 and nSpikes>2000")
        othercellSS = otherCells['LowAmpSS'].tolist()
        othercellSS = [x for x in othercellSS if (np.isnan(x) == False)]
        plot_categorical_scatter_with_mean([thalcellSS,PVcellSS,SOMcellSS,othercellSS], ['thalamus','AC-PV','AC-SOM','AC-unidentified'], colours = ['0.5','b','g','0.5'], xlabel='Cell type', ylabel='Suppression score', title='50dB Suppression')
    elif CASE==6:
        db = pd.read_hdf('/home/jarauser/src/jaratest/anna/analysis/all_clusters.h5','database',index_col=0)
        thalmice = db.query("subject=='band022' or subject=='band023'")
        thalCells = thalmice.query("isiViolations<0.02 and nSpikes>2000 and clusterQuality>2.5 and atBestFreq==1")
        thalcellSS = thalCells['HighAmpFS'].tolist()
        PVmice = db.query("subject=='band004' or subject=='band026'")
        PVCells = PVmice.query("laserResponse==1 and atBestFreq==1 and isiViolations<0.02 and clusterQuality>2.5 and nSpikes>2000")
        PVcellSS = PVCells['HighAmpFS'].tolist()
        SOMmice = db.query("subject=='band005' or subject=='band015' or subject=='band016' or subject=='band027' or subject=='band028' or subject=='band029' or subject=='band030' or subject=='band031'")
        SOMCells = SOMmice.query("isiViolations<0.02 and clusterQuality>2.5 and atBestFreq==1 and laserResponse==1 and nSpikes>2000")
        SOMcellSS = SOMCells['HighAmpFS'].tolist()
        notThalMice = db.query("subject!='band022' and subject!='band023'")
        otherCells = notThalMice.query("isiViolations<0.02 and clusterQuality>2.5 and atBestFreq==1 and laserResponse!=1 and nSpikes>2000")
        othercellSS = otherCells['HighAmpFS'].tolist()
        othercellSS = [x for x in othercellSS if (np.isnan(x) == False)]
        plot_categorical_scatter_with_mean([thalcellSS,PVcellSS,SOMcellSS,othercellSS], ['thalamus','AC-PV','AC-SOM','AC-unidentified'], colours = ['0.5','b','g','0.5'], xlabel='Cell type', ylabel='Facilitation score', title='70dB Facilitation')
    elif CASE==7:
        db = pd.read_hdf('/home/jarauser/src/jaratest/anna/analysis/all_clusters.h5','database',index_col=0)
        thalmice = db.query("subject=='band022' or subject=='band023'")
        thalCells = thalmice.query("isiViolations<0.02 and nSpikes>2000 and clusterQuality>2.5 and atBestFreq==1")
        thalcellSS = thalCells['LowAmpFS'].tolist()
        PVmice = db.query("subject=='band004' or subject=='band026'")
        PVCells = PVmice.query("laserResponse==1 and atBestFreq==1 and isiViolations<0.02 and clusterQuality>2.5 and nSpikes>2000")
        PVcellSS = PVCells['LowAmpFS'].tolist()
        SOMmice = db.query("subject=='band005' or subject=='band015' or subject=='band016' or subject=='band027' or subject=='band028' or subject=='band029' or subject=='band030' or subject=='band031'")
        SOMCells = SOMmice.query("isiViolations<0.02 and clusterQuality>2.5 and atBestFreq==1 and laserResponse==1 and nSpikes>2000")
        SOMcellSS = SOMCells['LowAmpFS'].tolist()
        SOMcellSS = [x for x in SOMcellSS if (np.isnan(x) == False)]
        notThalMice = db.query("subject!='band022' and subject!='band023'")
        otherCells = notThalMice.query("isiViolations<0.02 and clusterQuality>2.5 and atBestFreq==1 and laserResponse!=1 and nSpikes>2000")
        othercellSS = otherCells['LowAmpFS'].tolist()
        othercellSS = [x for x in othercellSS if (np.isnan(x) == False)]
        plot_categorical_scatter_with_mean([thalcellSS,PVcellSS,SOMcellSS,othercellSS], ['thalamus','AC-PV','AC-SOM','AC-unidentified'], colours = ['0.5','b','g','0.5'], xlabel='Cell type', ylabel='Facilitation score', title='50dB Facilitation')
        
        
        
        
        