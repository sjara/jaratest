'''
This script is to test functions for the project
'''

#Python
import numpy as np
import matplotlib.pyplot as plt
#from jaratoolbox import pupilanalysis


proc = np.load('./fromFullVideos/chad050_020-5_proc.npy', allow_pickle = True).item()
#Note: the proc.npy is the output file generated from facemap.



pupil = proc['pupil'][0] # Dic.
pArea = pupil['area']    # numpy.array. Contains calculation of the pupil area in each frame of the video.
#pAreaa = pArea[:-5] # Elimination of last 5 elements of array. Fixes infinite line length (X axis).
blink = proc['blink'][0] # numpy.array. Contains calculation of the sync signal in each frame of the video.
blink1 = proc['blink']   # List.
blink2 = np.array(blink).T # Creates transpose matrix of blink. Necessary for plotting.
#blink2_a = blink[:-5] # Elimination of last 5 elements of array. Fixes infinite line length (Y axis).


nframes = len(pArea) # Contains length of pArea variable (equivalent to the blink variable).
frameVec = np.arange(0, nframes, 1) # Vector of the total frames from the video.
framerate = 30 # frame rate of video
timeVec = (frameVec * 1)/framerate # Time Vector to calculate the length of the video .

blink2Bool = np.logical_and(blink2>103000, blink2<143000) # Boolean values from the blink2 variable where True values will be within the established range.
blink2RangeValues = np.diff(blink2Bool) # Determines the start and ending values (as the boolean value True) where the sync signal is on. 
indicesValueSyncSignal = np.flatnonzero(blink2RangeValues) # Provides all the indices of numbers assigned as 'True' from the blink2_binary variable.

'''
with np.printoptions(threshold=np.inf): # Use the following code to show all the elements within a large array
    print(arr)
'''

def onset_values(array, k): 

     '''
     Helps to find onset start values of the sync singal in any given array: 
     Args: 
     array = array that contains data of the sync signal
     k = step number to create the range from 0 to n index of the given array
     Returns:
     startValuesVec = an array of the indices containing the start onset values of the sync signal.
     '''
     firstIndexValue = 0 
     lastIndexValue = len(array)-1 
     stepNumber = k
     startIndicesValues = range(firstIndexValue, lastIndexValue, stepNumber)
     startIndicesVec = np.array(startIndicesValues)
     onsetStartValues = np.take(array, startIndicesVec)
     return (onsetStartValues)

syncOnsetValues = onset_values(indicesValueSyncSignal, 2)
timeOfBlink2Event = timeVec[syncOnsetValues] # Provides the time values in which the sync signal is on.
timeRange = np.array([-1, 2]) # Range of time window, one second before the sync signal is on and two seconds after is on.

samplingRate = 1/(timeVec[1]-timeVec[0])
windowSampleRange = samplingRate*np.array(timeRange) 
windowSampleVec = np.arange(*windowSampleRange, dtype=int)
windowTimeVec = windowSampleVec/samplingRate
nSamples = len(windowTimeVec)
nTrials = len(timeOfBlink2Event)



def eventlocked_signal(timeVec, signal, eventOnsetTimes, windowTimeRange):
    '''
    Make array of signal traces locked to an event.
    Args:
        timeVec (np.array): time of each sample in the signal.
        signal (np.array): samples of the signal to process.
        eventOnsetTimes (np.array): time of each event.
        windowTimeRange (list or np.array): 2-element array defining range of window to extract.
    Returns: 
        windowTimeVec (np.array): time of each sample in the window w.r.t. the event.
        lockedSignal (np.array): extracted windows of signal aligned to event. Size (nSamples,nEvents)
    '''
    samplingRate = 1/(timeVec[1]-timeVec[0])
    windowSampleRange = samplingRate*np.array(windowTimeRange) 
    windowSampleVec = np.arange(*windowSampleRange, dtype=int)
    windowTimeVec = windowSampleVec/samplingRate
    nSamples = len(windowTimeVec)
    nTrials = len(eventOnsetTimes)
    lockedSignal = np.empty((nSamples,nTrials))
    for inde,eventTime in enumerate(eventOnsetTimes):
        eventSample = np.searchsorted(timeVec, eventTime)
        thiswin = windowSampleVec + eventSample
        lockedSignal[:,inde] = signal[thiswin]
        #print('this is eventsample:',eventSample)
        #print('this is thiswin:;',thiswin)
        #print(thiswin.shape)
    return (windowTimeVec, lockedSignal)

windowTimeVec, windowed_signal = eventlocked_signal(timeVec, pArea, timeOfBlink2Event, timeRange)


preSignal = windowed_signal[0:30] # Takes the values of the pArea between [-1s to 0s) within the time window
postSignal = windowed_signal[30:90] # Takes the values of the pArea between [0s to 2s] within the time window
averagePreSignal = preSignal.mean(axis = 0)
averagePostSignal = postSignal.mean(axis = 0)
dataToPlot = [averagePreSignal, averagePostSignal]
xlabels = ['Pre Signal', 'Post Signal']


def conditions_Plotting(preArray, postArray): 
     xLabelsToPlot = ['Pre Signal', 'Post Signal'] 
     dataToPlot = [preArray, postArray] 
     fig, trials = plt.subplots(1,1) 
     trials.plot(xLabelsToPlot, dataToPlot, marker = 'o', linewidth=1) 
     trials.set(title = 'Average Pupil Area Vs Pre and Post-signal onset', ylabel = 'Mean Pupil Area') 
     plt.show() 
     return(plt.show())

PrePostSignalpArea = conditions_Plotting(averagePreSignal, averagePostSignal)
 
'''
def conditions_Plotting(preArray, postArray, k): 
    ...:     for i in range(k): 
    ...:         verts = [(preArray[i], postArray[i])] 
    ...:         for i in verts: 
    ...:             codes = [Path.MOVETO, Path.LINETO,  Path.CLOSEPOLY] 
    ...:             pathToPlot = Path(verts, codes) 
    ...:             fig, ax = plt.subplots() 
    ...:             patch = patches.PathPatch(path, facecolor='orange', lw=2) 
    ...:             ax.add_patch(patch) 
    ...:             plt.show() 
    ...:     return(plt.show())
'''    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
'''
def data_Trials(array, k, r): 
     
     Allows to obtain all values from a given trial/column 
     args: 
     array = array that contains the columns with the data of interest 
     k = number of columns of the given array 
     r = number of rows of the given array 
     returns: 
     trialsArr = contains a list of each column with their values 
     
     trialsArr = [] 
     for j in range(k): 
         for i in range(r): 
             trialsArr.append(array[i][j]) 
         #trialsArr.append('This is a trial') 
     return(trialsArr)

trialsValues = data_Trials(windowed_signal, 114, 90) # len(trialsValues) = ~10374 and 10374/90 = ~114. Each trial contains 90 values. The division above must be almost equal to the same amount of columns/trials because it must contain the value for each column/trial (in this case, is 114)

def get_Trials(array, totalValues): 
      
     This will create a dic with each trial 
     args: 
     array = array with the data of the trials 
     totalValues = number provided by len(array) 
     returns: 
     locals = will contain a dic with the name of each trial containing their values 
      
     arrayIndices = np.arange(0, totalValues, 1) 
     for i in arrayIndices: 
         locals()['trial'+str(i)] = array[i:i+90] 
     return(locals())

numberOfTrials = get_Trials(trialsValues, 114) #pAreaEachTrial
'''
'''
def prepos_Trials(dic): 
    ...:     arrTrials = dic 
    ...:     arrKeys = dic.keys() 
    ...:     for key,value in arrTrials.items(): 
    ...:         preTrials = dic[arrKeys][value:val+30] 
    ...:         postTrials = dic[arrKeys][30:90] 
    ...:     return(preTrials, postTrials)
'''















'''
#WORKS: function to plot in bars and the data used
beforeOnsetTimeValues = windowed_signal[0:30] # Takes the values of the pArea between [-1s to 0s) within the time window
afterOnsetTimeValues = windowed_signal[30:90] # Takes the values of the pArea between [0s to 2s] within the time window
meanSignalBeforeOnset = beforeOnsetTimeValues.mean(axis = 0) # Mean Values for each column in the time window -1 to 0. Creates an an average signal
meanSignalAfterOnset = afterOnsetTimeValues.mean(axis = 0) # Mean Values for each column in the time window 0 to 2. Creates an avarage signal
meanValueBeforeOnset = meanSignalBeforeOnset.mean() # Mean value before signal onset 
meanValueAfterOnset = meanSignalAfterOnset.mean() # Mean value after signal onset
labelsName = ('Stimulus off', 'Stimulus onset')
xlabels = np.arange(len(labelsName))
width = 0.35


def meanValue_Plot(slicedRange1, slicedRange2, title, labelsx, labelsy, dataPlot, c1, c2):

     meanSignal1 = slicedRange1.mean(axis = 0) 
     meanSignal2 = slicedRrange2.mean(axis = 0) 
     meanValue1 = meanSignal1.mean() 
     meanValue2 = meanSignal2.mean()
     conditions = (c1, c2) 
     plt.bar(conditions, dataPlot, width = 0.35, align = 'center') 
     plt.title(title) 
     plt.xlabel(labelsx) 
     plt.ylabel(labelsy) 
     return (plt.show()) 

toPlot = meanValue_Plot(windowed_signal[0:30], windowed_signal[30:90], 'a', 'b', 'c', meanValueAfterOnset, 'alal', 'foo')   
'''


'''
#WORKS: to plot in bars
fig, ax = plt.subplots()
plot1 = ax.bar(xlabels[0], meanValueBeforeOnset, width, align = 'center')
plot2 = ax.bar(xlabels[1], meanValueAfterOnset, width, align = 'center')
ax.set_title('Average Pupil Area Vs Conditions')
ax.set_xticks(xlabels)
ax.set_xticklabels(labelsName)
ax.set_ylabel('Pupil Area')

plt.show()
'''
