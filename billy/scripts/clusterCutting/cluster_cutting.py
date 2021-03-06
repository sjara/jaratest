import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
import itertools

class ClusterCutter(object):
    '''
    Nick Ponvert 05-10-2015
    
    GUI window for cutting a cluster. Accepts an N by M array of points, 
    where N is the number of spikes and M is the number of attributes 
    (i.e. peak amplitude on each wire). The window allows the user to click
    to define a set of points that are used to form a convex hull,
    and the cluster is cut using the hull. Multiple cuts can be performed in 
    any of the different dimensions. After cutting is complete, the 
    attribute self.inCluster will contain a boolean list which can be used to 
    select only the spikes that are in the cut cluster. 
    '''

    def __init__(self, points):

        plt.close("all")
        #Scatter the points
        self.points = points

        #Figure out the dimensions of the data and how many combos there are 
        self.numDims=self.points.shape[1]
        self.combinations=[c for c in itertools.combinations(range(self.numDims), 2)]
        self.maxDim=len(self.combinations)-1

        #Start with the first combination
        self.dimNumber=0
        
        #All points start inside the cluster
        self.inCluster=np.ones(len(self.points), dtype=bool)
        self.outsideCluster=np.logical_not(self.inCluster)
        
        #Preserve the last cluster state for undo
        self.oldInsideCluster=self.inCluster
        self.oldOutsideCluster=self.outsideCluster
    
        #Make the fig and ax, and draw the initial plot
        self.fig=plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.draw_dimension(self.dimNumber)

        #Start the mouse handle.r and make an attribute to hold click pos
        self.mpid=self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.mouseClickData=[]

        #Start the key press handler
        self.kpid = self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

        #show the plot
        plt.show()

    def on_click(self, event):
        '''
        Method to record mouse clicks in the mouseClickData attribute
        and plot the points on the current axes
        '''
        
        self.mouseClickData.append([event.xdata, event.ydata])
        self.ax.plot(event.xdata, event.ydata, 'r+')
        self.fig.canvas.draw()

    
    def on_key_press(self, event):
        '''
        Method to listen for keypresses and take action
        '''
        
        #Function to cut the cluster
        if event.key=='c':
            #Only cut the cluster if there are 3 points or more
            if len(self.mouseClickData)>2:
                hullArray=np.array(self.mouseClickData)
                self.cut_cluster(self.points[:, self.combinations[self.dimNumber]], hullArray)
                self.draw_dimension(self.dimNumber)
                self.mouseClickData=[]
            else:
                pass
            
        #Function to undo the last cut
        if event.key=='u':
            self.mouseClickData=[]
            self.inCluster=self.oldInsideCluster
            self.outsideCluster=self.oldOutsideCluster
            self.draw_dimension(self.dimNumber)

        #Functions to cycle through the dimensions
        elif event.key=="<":
            if self.dimNumber>0:
                self.dimNumber-=1
            else:
                self.dimNumber=self.maxDim

            self.draw_dimension(self.dimNumber)
                

        elif event.key=='>':
            if self.dimNumber<self.maxDim:
                self.dimNumber+=1
            else:
                self.dimNumber=0

            self.draw_dimension(self.dimNumber)


    def draw_dimension(self, dimNumber):
        '''
        Method to draw the points on the axes using the current dimension number
        '''
    
        #Clear the plot and any saved mouse click data for the old dimension
        self.ax.cla()
        self.mouseClickData=[]
        
        #Find the point array indices for the dimensions to be plotted
        dim0 = self.combinations[self.dimNumber][0]
        dim1 = self.combinations[self.dimNumber][1]

        #Plot the points in the cluster in green, and points outside as light grey
        self.ax.plot(self.points[:,dim0][self.inCluster], self.points[:, dim1][self.inCluster], 'g.')
        self.ax.plot(self.points[:, dim0][self.outsideCluster], self.points[:,dim1][self.outsideCluster], marker='.', color='0.8', linestyle='None')

        #Label the axes and draw
        self.ax.set_xlabel('Dimension {}'.format(dim0))
        self.ax.set_ylabel('Dimension {}'.format(dim1))
        plt.title('press c to cut, u to undo last cut, < or > to switch dimensions')
        self.fig.canvas.draw()
        
    
    def cut_cluster(self, points, hull):
        ''' Method to take the current points from mouse input, 
        convert them to a convex hull, and then update the inCluster and 
        outsideCluster attributes based on the points that fall within 
        the hull'''

        #If the hull is not already a Delaunay instance, make it one
        if not isinstance(hull, Delaunay):
            hull=Delaunay(hull)

        #Save the old cluster for undo
        self.oldInsideCluster=self.inCluster
        self.oldOutsideCluster=self.outsideCluster

        #Find the ponts that are inside the hull
        inHull = hull.find_simplex(points)>=0

        #Only take the points that are inside the hull and the cluster
        #so we can cut from different angles and preserve old cuts
        newInsidePoints = self.inCluster & inHull
        self.inCluster = newInsidePoints
        self.outsideCluster = np.logical_not(self.inCluster)

    def output_cut_points(self):
        '''Method to output boolean of cut spikes.'''
        return self.inCluster

            

if __name__=='__main__':
    mean=[1, 1, 1, 1]
    cov=np.random.random([4, 4])
    data = np.random.multivariate_normal(mean, cov, 1000)
    cw = ClusterCutter(data)

