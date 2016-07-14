'''
Simple graphical interface example using PySide

For PySide documentation, see:
http://srinikom.github.io/pyside-docs/PySide/QtGui/
'''

__author__ = 'Santiago Jaramillo'
__date__ = '2015-01-13'


import sys
from PySide import QtCore 
from PySide import QtGui 
import signal
import os
import numpy as np
import plottingRasterAndHist
import matplotlib.pyplot as plt


def plotting_function(someValue):
    '''
    The plotting function should be in a separate file, because we want people to
    be able to load, analyze and plot the data from the command line without a GUI.

    For this example we just have it as a separate method in the same file.
    '''
    import matplotlib.pyplot as plt
    plt.clf()
    plt.plot(np.random.rand(someValue),'o-')
    plt.draw()
    plt.show()


class graphUI(QtGui.QMainWindow):
    '''
    This is a simple graphical interface that opens a plot when a button is pressed.
    Note that this interface should not contain the data or analysis. It calls other
    methods to do that, such as plotting_function()
    '''
    def __init__(self, parent=None, paramfile=None, paramdictname=None):
        super(graphUI, self).__init__(parent)

        # -- Add graphical widgets to main window --
        self.centralWidget = QtGui.QWidget()
        layoutMain = QtGui.QVBoxLayout()
        self.allFreqButtonPressed = False
        self.compareButtonPressed = False

        self.oneLabel = QtGui.QLabel('Number of data points')
        self.oneNumeric = QtGui.QLineEdit()
        self.oneNumeric.setText('4')
        self.oneButton = QtGui.QPushButton('Plot')
        self.oneButton.clicked.connect(self.plot_data)

        layoutMain.addWidget(self.oneLabel)
        layoutMain.addWidget(self.oneNumeric)
        layoutMain.addWidget(self.oneButton)

        self.plotButton = QtGui.QPushButton('Plot Data')
        self.plotButton.clicked.connect(self.plotting_data)
        self.subjectLabel = QtGui.QLabel('Subject Name')
        self.subjectNumeric = QtGui.QLineEdit()
        self.subjectNumeric.setText('test019')
        self.ephysSessionLabel = QtGui.QLabel('Ephys Session')
        self.ephysSessionNumeric = QtGui.QLineEdit()
        self.ephysSessionNumeric.setText('2014-12-24_17-11-53')
        self.behaviorSessionLabel = QtGui.QLabel('Behavior Session')
        self.behaviorSessionNumeric = QtGui.QLineEdit()
        self.behaviorSessionNumeric.setText('20141224a')
        self.allFreqButtonPressed = False
        self.allFreqButton = QtGui.QPushButton('All Frequencies Sorted in Raster')
        self.allFreqButton.setCheckable(True)
        self.allFreqButton.clicked.connect(self.plotFreqRaster)
        self.compareButtonPressed = False
        self.compareButton = QtGui.QPushButton('Compare Two Outcomes in Raster')
        self.compareButton.setCheckable(True)
        self.compareButton.clicked.connect(self.plotCompareRaster)
        self.tetrodeLabel = QtGui.QLabel('Tetrode Number')
        self.tetrodeNumeric = QtGui.QLineEdit()
        self.tetrodeNumeric.setText('1')
        self.freqLabel = QtGui.QLabel('Frequency to Plot (as index)')
        self.freqNumeric = QtGui.QLineEdit()
        self.freqNumeric.setText('0')

        self.trialsToUse1Label = QtGui.QLabel('trialsToUse1')
        self.trialsToUse1MenuBar = QtGui.QMenuBar()   
        self.trialsToUse2Label = QtGui.QLabel('trialsToUse2')
        self.trialsToUse2MenuBar = QtGui.QMenuBar()   
        self.rastorCenterLabel = QtGui.QLabel('Rastor Plot Centered on:')
        self.rastorCenterMenuBar = QtGui.QMenuBar()  

        self.binSizeLabel = QtGui.QLabel('Bin Size for Histogram')
        self.binSizeNumeric = QtGui.QLineEdit()
        self.binSizeNumeric.setText('0.1')
        self.startTimeLabel = QtGui.QLabel('Start Time for Time Range for Plotting Spikes in Rastor Plot')
        self.startTimeNumeric = QtGui.QLineEdit()
        self.startTimeNumeric.setText('-0.5')
        self.endTimeLabel = QtGui.QLabel('End Time for Time Range for Plotting Spikes in Rastor Plot')
        self.endTimeNumeric = QtGui.QLineEdit()
        self.endTimeNumeric.setText('1.0')
        self.startRangeLabel = QtGui.QLabel('Start Time for Time Range for Counting Spikes in Rastor Plot')
        self.startRangeNumeric = QtGui.QLineEdit()
        self.startRangeNumeric.setText('0.1')
        self.endRangeLabel = QtGui.QLabel('End Time for Time Range for Counting Spikes in Rastor Plot')
        self.endRangeNumeric = QtGui.QLineEdit()
        self.endRangeNumeric.setText('0.4')

        self.saveLabel = QtGui.QLabel('Save')

        layoutMain.addWidget(self.plotButton)
        layoutMain.addWidget(self.subjectLabel)
        layoutMain.addWidget(self.subjectNumeric)
        layoutMain.addWidget(self.ephysSessionLabel)
        layoutMain.addWidget(self.ephysSessionNumeric)
        layoutMain.addWidget(self.behaviorSessionLabel)
        layoutMain.addWidget(self.behaviorSessionNumeric)
        layoutMain.addWidget(self.allFreqButton)
        layoutMain.addWidget(self.compareButton)
        layoutMain.addWidget(self.tetrodeLabel)
        layoutMain.addWidget(self.tetrodeNumeric)
        layoutMain.addWidget(self.freqLabel)
        layoutMain.addWidget(self.freqNumeric)
        layoutMain.addWidget(self.trialsToUse1Label)
        layoutMain.addWidget(self.trialsToUse1MenuBar)
        layoutMain.addWidget(self.trialsToUse2Label)
        layoutMain.addWidget(self.trialsToUse2MenuBar)
        layoutMain.addWidget(self.rastorCenterLabel)
        layoutMain.addWidget(self.rastorCenterMenuBar)
        layoutMain.addWidget(self.binSizeLabel)
        layoutMain.addWidget(self.binSizeNumeric)
        layoutMain.addWidget(self.startTimeLabel)
        layoutMain.addWidget(self.startTimeNumeric)
        layoutMain.addWidget(self.endTimeLabel)
        layoutMain.addWidget(self.endTimeNumeric)
        layoutMain.addWidget(self.startRangeLabel)
        layoutMain.addWidget(self.startRangeNumeric)
        layoutMain.addWidget(self.endRangeLabel)
        layoutMain.addWidget(self.endRangeNumeric)
        layoutMain.addWidget(self.saveLabel)


        self.centralWidget.setLayout(layoutMain)
        self.setCentralWidget(self.centralWidget)

    def plot_data(self):
        oneValue = int(self.oneNumeric.text())
        plotting_function(oneValue)

    def plotFreqRaster(self):
        if (self.allFreqButtonPressed):
            self.allFreqButtonPressed = False
        else:
            self.allFreqButtonPressed = True

    def plotCompareRaster(self):
        if (self.compareButtonPressed):
            self.compareButtonPressed = False
        else:
            self.compareButtonPressed = True

    def plotting_data(self):
       #plottingAllFreqCompareRaster(subject, ephys session, behavior session, tetrode number, index of frequency to plot, bin size for histogram, start time of when to count spikes in raster, end time of when to count spikes in raster, start time of when to plot spikes in raster, end time of when to plot spikes in raster)
       tetrodeNum = int(self.tetrodeNumeric.text())
       freqNum = int(self.freqNumeric.text())
       binSize = float(self.binSizeNumeric.text())
       startTime = float(self.startTimeNumeric.text())
       endTime = float(self.endTimeNumeric.text())
       startRange = float(self.startRangeNumeric.text())
       endRange = float(self.endRangeNumeric.text())
       plt.clf()

       if (self.compareButtonPressed):
           if (self.allFreqButtonPressed):
               plottingRasterAndHist.plottingAllFreqCompareRaster(self.subjectNumeric.text(),self.ephysSessionNumeric.text(),self.behaviorSessionNumeric.text(),tetrodeNum,freqNum,binSize,startTime,endTime,startRange,endRange)
           else:
               plottingRasterAndHist.plottingOneFreqCompareRaster(self.subjectNumeric.text(),self.ephysSessionNumeric.text(),self.behaviorSessionNumeric.text(),tetrodeNum,freqNum,binSize,startTime,endTime,startRange,endRange)
       else:
           plottingRasterAndHist.plottingAllFreqRaster(self.subjectNumeric.text(),self.ephysSessionNumeric.text(),self.behaviorSessionNumeric.text(),tetrodeNum,freqNum,binSize,startTime,endTime,startRange,endRange)

    def closeEvent(self, event):
        '''
        Executed when closing the main window.
        This method is inherited from QtGui.QMainWindow, which explains
        its camelCase naming.
        '''
        event.accept()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL) # Enable Ctrl-C
    app=QtGui.QApplication.instance() # checks if QApplication already exists 
    if not app: # create QApplication if it doesnt exist 
        app = QtGui.QApplication(sys.argv)
    graphingUI = graphUI()
    graphingUI.show()
    sys.exit(app.exec_())

