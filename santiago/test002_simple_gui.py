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


def plotting_function(someValue):
    '''
    The plotting function should be in a separate file, because we want people to
    be able to load, analyze and plot the data from the command line without a GUI.

    For this example we just have it as a separate method in the same file.
    '''
    import matplotlib.pyplot as plt
    plt.plot(np.random.rand(someValue),'o-')
    plt.draw()
    plt.show()


class myWindow(QtGui.QMainWindow):
    '''
    This is a simple graphical interface that opens a plot when a button is pressed.
    Note that this interface should not contain the data or analysis. It calls other
    methods to do that, such as plotting_function()
    '''
    def __init__(self, parent=None, paramfile=None, paramdictname=None):
        super(myWindow, self).__init__(parent)

        # -- Add graphical widgets to main window --
        self.centralWidget = QtGui.QWidget()
        layoutMain = QtGui.QVBoxLayout()

        self.oneLabel = QtGui.QLabel('Number of data points')
        self.oneNumeric = QtGui.QLineEdit()
        self.oneNumeric.setText('4')
        self.oneButton = QtGui.QPushButton('Plot')
        self.oneButton.clicked.connect(self.plot_data)

        layoutMain.addWidget(self.oneLabel)
        layoutMain.addWidget(self.oneNumeric)
        layoutMain.addWidget(self.oneButton)

        self.centralWidget.setLayout(layoutMain)
        self.setCentralWidget(self.centralWidget)

    def plot_data(self):
        oneValue = int(self.oneNumeric.text())
        plotting_function(oneValue)

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
    mywin = myWindow()
    mywin.show()
    sys.exit(app.exec_())

