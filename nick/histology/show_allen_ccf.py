import nrrd
import numpy as np
from matplotlib import pyplot as plt

ccfData = nrrd.read('/home/nick/data/jarahubdata/atlas/AllenCCF_25/coronal_average_template_25.nrrd')
ccf = ccfData[0]

# corticalBoundsData = nrrd.read('/home/nick/data/jarahubdata/atlas/AllenCCF_25/coronal_isocortex_boundary_25.nrrd')
corticalBoundsData = nrrd.read('/home/nick/data/jarahubdata/atlas/AllenCCF_25/coronal_laplacian_25.nrrd')
cortData = corticalBoundsData[0]


# plt.clf()
# plt.imshow(np.rot90(ccf[:,:,257], -1))
# plt.show

class CCFDisplay(object):

    def __init__(self, atlas, corticalBoundsAtlas=None):

        self.maxSlice = np.shape(atlas)[2]-1
        self.sliceNum=0

        self.atlas = atlas
        self.corticalBoundsAtlas = corticalBoundsAtlas
        if self.corticalBoundsAtlas is not None:
            self.corticalBoundsAtlas = np.ma.masked_where(self.corticalBoundsAtlas==0, self.corticalBoundsAtlas)

        self.fig=plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.hold(True)
        self.show_slice(self.sliceNum)

        self.mpid=self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.mouseClickData=[]

        #Start the key press handler
        self.kpid = self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

        #show the plot
        self.fig.show()

    def on_click(self, event):
        '''
        Method to record mouse clicks in the mouseClickData attribute
        and plot the points on the current axes
        '''
        self.mouseClickData.append([event.xdata, event.ydata])
        ymin, ymax = self.ax.get_ylim()
        xmin, xmax = self.ax.get_xlim()
        self.ax.plot(event.xdata, event.ydata, 'r+')
        print "[{}, {}, {}]".format(int(event.xdata), int(event.ydata), int(self.sliceNum))
        self.ax.set_ylim([ymin, ymax])
        self.ax.set_xlim([xmin, xmax])
        self.fig.canvas.draw()

    def on_key_press(self, event):
        '''
        Method to listen for keypresses and take action
        '''

        #Functions to cycle through the slices
        if event.key==",":
            if self.sliceNum>0:
                self.sliceNum-=1
            else:
                self.sliceNum=self.maxSlice

            self.show_slice(self.sliceNum)

        if event.key=="<":
            if self.sliceNum>10:
                self.sliceNum-=10
            else:
                self.sliceNum=self.maxSlice

            self.show_slice(self.sliceNum)

        elif event.key=='.':
            if self.sliceNum<self.maxSlice:
                self.sliceNum+=1
            else:
                self.sliceNum=0

            self.show_slice(self.sliceNum)

        elif event.key=='>':
            if self.sliceNum<self.maxSlice-10:
                self.sliceNum+=10
            else:
                self.sliceNum=0

            self.show_slice(self.sliceNum)

    def show_slice(self, sliceNum):
        '''
        Method to draw one slice from the atlas
        '''

        #Clear the plot and any saved mouse click data for the old dimension
        self.ax.cla()
        self.mouseClickData=[]

        #Draw the image
        self.ax.imshow(np.rot90(self.atlas[:,:,sliceNum], -1), 'gray')

        self.ax.hold(1)
        self.ax.imshow(np.rot90(self.corticalBoundsAtlas[:,:,sliceNum], -1), 'jet', alpha=0.2)



        #Label the axes and draw
        plt.title('< or > to move through the stack\nSlice: {}'.format(sliceNum))
        self.fig.canvas.draw()

ccfd = CCFDisplay(ccf, cortData)
