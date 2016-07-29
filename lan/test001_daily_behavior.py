'''
For Daily Behavior Monitoring.
Loads behavior data from mounted jarahub/data/behavior for animals of interest, plot psychometric curve. An alternative is to directly use the mounted drive and change settings.BEHAVIOR_PATH within the script.
'''
import os
from shutil import copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import behavioranalysis
reload(behavioranalysis)
from jaratoolbox import loadbehavior
reload(loadbehavior)
from jaratoolbox import settings

'''
FREQCOLORS = [colorpalette.TangoPalette['Chameleon3'],
              colorpalette.TangoPalette['ScarletRed1'],
              colorpalette.TangoPalette['SkyBlue2'] ]
'''

class DailyBehaviorReport(object): 
    '''
    Object for loading and ploting daily behavior data for animals of interest.
    subjects should be a string or a list of strings of animal name(s).
    sessions should be a string or a list of strings of sessions to analyze.
    '''
    def __init__(self, subjects, sessions, outputDir='/home/languo/data/behaviorsum', paradigm = '2afc'):
        self.experimenter = settings.DEFAULT_EXPERIMENTER
        self.outputDir = outputDir
        if isinstance(subjects,str):
            self.subjects = [subjects]
        if isinstance(sessions,str):
            self.sessions = [sessions]
        self.behavFileName = []
        self.paradigm = paradigm
        
    def set_file_names(self):
        dataFileFormat = '{0}_{1}_{2}.h5'
        for inds,thisSession in enumerate(self.sessions):
            for inda, thisSubject in enumerate(self.subjects):
               self.behavFileName.extend(dataFileFormat.format(thisSubject,self.paradigm,thisSession))
        return self.behavFileName

    def copy_behav_file(self):
    '''
    This is specific to Lan's computer, 
    using a mounted drive to jarahub/data behavior. 
    Have to copy the files of interest to default behavior dir.
    '''
        ALLBEHAV_PATH = '/home/languo/data/mnt/jarahubdata'
        for fileName in self.behavFileName:
            behavFileSrc = os.path.join(ALLBEHAV_PATH, self.experimenter, thisSubject,fileName)
            behavFile = os.path.join(settings.BEHAVIOR_PATH,self.experimenter,self.subject,fileName)
            shutil.copy(behavFileSrc, behavFile)

    def behav_sum(self):
        behavioranalysis.behavior_summary(self.subjects, self.sessions, outputDir=self.outputDir, paradigm=self.paradigm)

'''
    def plot_freq_psycurve(self):
        for fileName in self.behavFileName:
            behavFile = os.path.join(settings.BEHAVIOR_PATH,self.experimenter,self.subject,fileName)
            bdata = loadbehavior.BehaviorData(behavFile)
            (pline, pcaps, pbars, pdots) = behavioranalysis.plot_frequency_psycurve(bdata)
'''    

if __name__ == "__main__":

    CASE=1
    if CASE==1:
        sujects = ['adap007', 'adap009']
        sessions = '20150626a'
        BehavToday = DailyBehaviorReport(subjects, sessions)
        
   
