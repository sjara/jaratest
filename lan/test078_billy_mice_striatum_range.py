'''
This scripts stores the 'striatum range' for all of billy's mice. 
Striatum range was calculated based on the method described in http://jarahub.uoregon.edu/wiki/Report_2016-07-26:_tetrode_depth_calculation_and_scripts; basically this is the range of depths at which each tetrode was in the auditory striatum in a particular mouse.

Lan Guo 20170109
'''
import pandas as pd
import numpy as np

allAnimals = []

oneAnimal = dict(animalName='test089',
             tetrodeLengthList=np.array([0.110,0.310,0.460,0.570,0.230,0.430,0.000,0.000]),
                 depthRangeLongestTt=(2.38,3.14))
allAnimals.append(oneAnimal)


oneAnimal = dict(animalName='test059',
                 tetrodeLengthList=np.array([0.100,0.510,0.610,0.610,0.190,0.930,0.280,0.000]),
                 depthRangeLongestTt=(2.6,3.43))
allAnimals.append(oneAnimal)


oneAnimal = dict(animalName='test017',
                 tetrodeLengthList=np.array([0.504,0.000,0.209,0.209,0.209,0.705,0.459,0.504]),
                 depthRangeLongestTt=(3.265,3.83))
allAnimals.append(oneAnimal)


oneAnimal = dict(animalName='adap020',
                 tetrodeLengthList=np.array([0.210,0.230,0.000,0.480,0.380,0.610,0.480,0.380]),
                 depthRangeLongestTt=(2.6,3.71))
allAnimals.append(oneAnimal)


oneAnimal = dict(animalName='adap015',
                 tetrodeLengthList=np.array([1.260,0.260,0.540,0.340,0.000,0.240,0.110,0.320]),
                 depthRangeLongestTt=(2.0,3.00))
allAnimals.append(oneAnimal)


oneAnimal = dict(animalName='adap013',
                 tetrodeLengthList=np.array([0.420,0.530,0.000,0.080,0.490,0.140,0.230,0.360]),
                 depthRangeLongestTt=(2.0,3.11))
allAnimals.append(oneAnimal)


oneAnimal = dict(animalName='adap017',
                 tetrodeLengthList=np.array([0.050,0.000,0.600,0.190,0.140,0.410,0.310,0.430]),
                 depthRangeLongestTt=(2.0,3.17))
allAnimals.append(oneAnimal)


oneAnimal = dict(animalName='test055',
                 tetrodeLengthList=np.array([0.170,0.170,0.000,0.050,0.090,0.170,0.170,0.170]),
                 depthRangeLongestTt=(2.35,3.27))
allAnimals.append(oneAnimal)


oneAnimal = dict(animalName='test053',
                 tetrodeLengthList=np.array([0.140,0.000,0.320,0.440,0.260,0.640,0.580,0.190]),
                 depthRangeLongestTt=(2.0,3.27))
allAnimals.append(oneAnimal)


tLengthMatrix = np.vstack((oneAnimal['tetrodeLengthList'] for oneAnimal in allAnimals))
allAnimalsDb = pd.DataFrame(tLengthMatrix, columns=['1','2','3','4','5','6','7','8'])
allAnimalsDb['animalName'] = np.array([oneAnimal['animalName'] for oneAnimal in allAnimals])
allAnimalsDb['strTop'], allAnimalsDb['strBottom'] = zip(*[oneAnimal['depthRangeLongestTt'] for oneAnimal in allAnimals])

allAnimalsDb.to_csv('/home/languo/data/ephys/billy_mice_striatum_range.csv')


'''
for oneAnimal in allAnimals:
    #depthRangeEachTt = [oneAnimal['depthRangeLongestTt']-tetrodeOffset for tetrodeOffset in oneAnimal['tetrodeLengthList']]
    #thisMouseDb = pd.DataFrame(depthRangeEachTt).transpose()
    #thisMouseDb.columns=['Tt1','Tt2','Tt3','Tt4','Tt5','Tt6','Tt7','Tt8']
    thisMouseDb = pd.DataFrame((oneAnimal['tetrodeLengthList'][:,np.newaxis]), columns=['Tt1','Tt2','Tt3','Tt4','Tt5','Tt6','Tt7','Tt8'], index=[0]) #Cannot make a df from a one-dim np array??!!
    thisMouseDb['animalName'] = oneAnimal['animalName']
    thisMouseDb['strRange'] = oneAnimal['depthRangeLongestTt']
    allAnimalsDb = allAnimalsDb.append(thisMouseDb)
'''
