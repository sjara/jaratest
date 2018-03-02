import os
import matplotlib.image as mpimg
import numpy as np
import pandas as pd
from jaratoolbox import settings
from jaratest.nick.utils import allenPlateNames

STUDY_NAME = '2018thstr'
dbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, 'celldatabase.h5')
db = pd.read_hdf(dbPath, key='dataframe')

goodLaser = db.query('isiViolations<0.02 and spikeShapeQuality>2 and pulsePval<0.05 and trainRatio>0.8')

goodLaserThalSR = goodLaser.query("brainArea=='rightThal' and noisePval<0.05")
goodLaserACSR = goodLaser.query("brainArea=='rightAC' and noisePval<0.05")

# groups = goodLaserThalSR.groupby(['subject', 'date', 'tetrode', 'depth'])
# groups = goodLaserThalSR.groupby(['subject', 'date', 'tetrode'])
groups = goodLaserACSR.groupby(['subject', 'date', 'tetrode'])

# for name, group in groups:
#     print len(group)
#     print "Group: {} {} TT{}".format(name[0], name[1], name[2])
#     print "Max depth: {}".format(np.unique(group['maxDepth']))
#     print np.unique(group['info'])
#     print "\n"

def convertAllenZ(allenZ):
    '''
    '''
    startPlate = 576986019
    plateSpacing = 40
    webPlateInd = int(np.round((allenZ - 2) / 4.))
    return allenPlateNames.allenPlateNames[webPlateInd]

#     # atlasHTML = 'atlas.brain-map.org/atlas?atlas=602630314#atlas=602630314&plate={}'.format(plateNum)

# class RecordingTractImage(object):

#     def __init__(self, imFn):


#         self.imFn = imFn
#         self.fig=plt.figure()
#         self.ax = self.fig.add_subplot(111)
#         self.ax.hold(True)
#         self.image = mpimg()
#         self.image = mpimg.imread(self.imFn)
#         self.show_image(self.image)

#         self.mpid=self.fig.canvas.mpl_connect('button_press_event', self.on_click)
#         self.mouseClickData=[]

#         #Start the key press handler
#         self.kpid = self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

#         #show the plot
#         self.fig.show()

#     def on_click(self, event):
#         '''
#         Method to record mouse clicks in the mouseClickData attribute
#         and plot the points on the current axes
#         '''
#         self.mouseClickData.append([event.xdata, event.ydata])
#         ymin, ymax = self.ax.get_ylim()
#         xmin, xmax = self.ax.get_xlim()
#         self.ax.plot(event.xdata, event.ydata, 'r+')
#         print "[{}, {}, {}]".format(int(event.xdata), int(event.ydata), int(self.sliceNum))
#         self.ax.set_ylim([ymin, ymax])
#         self.ax.set_xlim([xmin, xmax])
#         self.fig.canvas.draw()

#     def on_key_press(self, event):
#         '''
#         Method to listen for keypresses and take action
#         '''

#         #Functions to cycle through the slices
#         if event.key=="c":
#             self.show_slice(self.sliceNum)

#         # if event.key=="<":
#         #     if self.sliceNum>10:
#         #         self.sliceNum-=10
#         #     else:
#         #         self.sliceNum=self.maxSlice

#         #     self.show_slice(self.sliceNum)

#         # elif event.key=='.':
#         #     if self.sliceNum<self.maxSlice:
#         #         self.sliceNum+=1
#         #     else:
#         #         self.sliceNum=0

#         #     self.show_slice(self.sliceNum)

#         # elif event.key=='>':
#         #     if self.sliceNum<self.maxSlice-10:
#         #         self.sliceNum+=10
#         #     else:
#         #         self.sliceNum=0

#         #     self.show_slice(self.sliceNum)
#         pass

#     def show_slice(self, sliceNum):
#         '''
#         Method to draw one slice from the atlas
#         '''

#         #Clear the plot and any saved mouse click data for the old dimension
#         self.ax.cla()
#         self.mouseClickData=[]

#         #Draw the image
#         self.ax.imshow(np.rot90(self.atlas[:,:,sliceNum], -1), 'gray')



