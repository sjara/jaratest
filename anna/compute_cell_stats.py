import pandas as pd
import numpy as np
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import bandwidths_analysis_v2 as bandan
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
def plot_categorical_scatter_with_mean(vals, categoryLabels, colours=None, xlabel=None, ylabel=None, title=None):
    import matplotlib.colors
    import scipy.stats
    numCategories = len(vals)
    if colours is None:
        colours = plt.cm.gist_rainbow(np.linspace(0,1,numCategories))
    for category in range(numCategories):
        edgeColour = matplotlib.colors.colorConverter.to_rgba(colours[category], alpha=0.5)
        plt.plot((category+1)*np.ones(len(vals[category])), vals[category], 'o', mec=edgeColour, mew = 4, mfc='none', ms=16)
        mean = np.mean(vals[category])
        sem = scipy.stats.sem(vals[category])
        plt.plot(category+1, mean, 'o', color=colours[category], mec=colours[category], ms=20)
        plt.errorbar(category+1, mean, yerr = sem, color=colours[category])
    plt.xlim(0,numCategories+1)
    ax = plt.gca()
    ax.set_xticks(range(1,numCategories+1))
    ax.set_xticklabels(categoryLabels, fontsize=16)
    if xlabel is not None:
        plt.xlabel(xlabel, fontsize=20)
    if ylabel is not None:
        plt.ylabel(ylabel, fontsize=20)
    if title is not None:
        plt.title(title)
    

if __name__ == '__main__':
    CASE = 5
    
    if CASE==0:    
        db = pd.read_csv('/home/jarauser/src/jaratest/anna/analysis/all_good_cells.csv',index_col=0)
        #db = db[(db['clusterQuality']<3)]
        #db = db[(db['clusterQuality']>0)]
        db = db[(db['clusterQuality']==1)]
        db.to_csv('/home/jarauser/src/jaratest/anna/analysis/good_cells_stats.csv')
    elif CASE==1:
        db = pd.read_csv('/home/jarauser/src/jaratest/anna/analysis/good_cells_stats.csv',index_col=0)
        db = db.reindex(columns=np.concatenate((db.columns.values,['atBestFreq','laserResponse','HighAmpSS','LowAmpSS','HighPeakLoc','LowPeakLoc','HighPeakSR','LowPeakSR'])))
        for indCell, cell in db.iterrows():
            print indCell
            suppressionStats, atBestFreq, laserResponse = bandan.suppression_stats(cell)
            if suppressionStats is not None:
                db.set_value(indCell, 'atBestFreq', atBestFreq)
                db.set_value(indCell, 'laserResponse', laserResponse)
                db.set_value(indCell, 'HighAmpSS', suppressionStats[1])
                db.set_value(indCell, 'HighPeakLoc', suppressionStats[3])
                db.set_value(indCell, 'HighPeakSR', suppressionStats[5])
                if suppressionStats[0] is not None:
                    db.set_value(indCell, 'LowAmpSS', suppressionStats[0])
                    db.set_value(indCell, 'LowPeakLoc', suppressionStats[2])
                    db.set_value(indCell, 'LowPeakSR', suppressionStats[4])
        db.to_csv('/home/jarauser/src/jaratest/anna/analysis/good_cells_stats.csv')
    elif CASE==2:
        db = pd.read_csv('/home/jarauser/src/jaratest/anna/analysis/good_cells_stats.csv')
        cell=db.loc[526]
        bandan.plot_bandwidth_report(cell)
        suppressionStats, atBestFreq, laserResponse = bandan.suppression_stats(cell)
    elif CASE==3:
        db = pd.read_csv('/home/jarauser/src/jaratest/anna/analysis/good_cells_stats.csv')
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
        db = pd.read_csv('/home/jarauser/src/jaratest/anna/analysis/good_cells_stats.csv')
        laserResponse = np.array(db['laserResponse'].tolist())
        subjects = np.array(db['subject'].tolist())
        PVsubj = np.where(subjects=='band004')[0]
        SOMsubj = np.where((subjects=='band005') | (subjects=='band015') | (subjects=='band016'))[0]
        PVlaser = laserResponse[PVsubj]
        SOMlaser = laserResponse[SOMsubj]
        PVcells = np.where(PVlaser==1)[0]
        SOMcells = np.where(SOMlaser==1)[0]
        SS = np.array(db['HighAmpSS'].tolist())
        PVSS = SS[PVsubj]
        SOMSS = SS[SOMsubj]
        PVcellSS = PVSS[PVcells]
        SOMcellSS = SOMSS[SOMcells]
        allCells = np.where(laserResponse==0)
        allCellsSS = SS[allCells]
        allCellsSS = allCellsSS[~np.isnan(allCellsSS)]
        plot_categorical_scatter_with_mean([PVcellSS,SOMcellSS], ['PV','SOM'], colours = ['b','g'], xlabel='Cell type', ylabel='Suppression score')
    elif CASE==5:
        db = pd.read_csv('/home/jarauser/src/jaratest/anna/analysis/good_cells_stats.csv')
        atBestFreq = np.array(db['atBestFreq'].tolist())
        highLoc = np.array(db['HighPeakSR'].tolist())
        bestCells = np.where(atBestFreq==1)
        bestHighLoc = highLoc[bestCells]

        numLowLoc = len(np.where(bestHighLoc<0.5)[0])
        numIntLoc = len(np.where((bestHighLoc>0.4) & (bestHighLoc<3))[0])
        numHighLoc = len(np.where(bestHighLoc>3)[0])
        
        print numLowLoc, numIntLoc, numHighLoc
        print len(bestCells[0])
        
        
        
        
        