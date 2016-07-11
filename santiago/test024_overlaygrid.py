
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import json

from jaratoolbox import histologyanalysis
reload(histologyanalysis)

imagesToAnalyze = ['/data/brainmix_data/test043_TL/p1-D1-01b.jpg',
                   '/data/brainmix_data/test043_TL/p1-D2-01b.jpg',
                   '/data/brainmix_data/test043_TL/p1-D3-01b.jpg']


ogrid = histologyanalysis.OverlayGrid(nRows=3,nCols=2)
ogrid.set_grid(imagesToAnalyze[0])

#ogrid.apply_grid(imagesToAnalyze[1])

'''
coordsEach = {}
for indimg,imgfile in enumerate(imagesToAnalyze):
    ogrid = histologyanalysis.OverlayGrid(imgfile,nRows=3,nCols=2)
    ogrid.set_grid()
    coordsEach[imgfile] = ogrid.coords
    #ogrid.coords = [[400,400],[600,800]]
dataStr = json.dumps(coordsEach,indent=0)

outputfile = '/var/tmp/test_grids.json'
fid = open(outputfile,'w')
fid.write(dataStr)
fid.close()
print 'Data saved to {0}'.format(outputfile)

#np.savez('/var/tmp/test000_grids.npz',filename=imgfile,coords=ogrid.coords)
'''



'''
GRIDCOLOR = [0,0.5,0.5]

img = mpimg.imread('/data/brainmix_data/test043_TL/p1-D1-01b.jpg')

fig = plt.gcf()
fig.clf()
plt.imshow(img)
plt.axis('tight')
plt.axis('equal')
plt.show()

coords = []

def onclick(event):
    #global ix, iy
    ix, iy = event.xdata, event.ydata
    print 'x = {0}, y = {1}'.format(ix, iy)
    global coords
    coords.append((ix, iy))
    if len(coords) == 2:
        #fig.canvas.mpl_disconnect(cid)
        draw_grid(coords)
        coords=[]
    #return coords

cid = fig.canvas.mpl_connect('button_press_event', onclick)

#coords = [ (200,600),(600,1000) ] 
#draw_grid(coords)

def draw_grid(coords,nRows=3,nCols=2):
    topleft,bottomright = coords
    xvals = np.linspace(topleft[0],bottomright[0],nCols+1)
    yvals = np.linspace(topleft[1],bottomright[1],nRows+1)
    holdStatus = plt.ishold()
    plt.hold(True)
    for yval in yvals:
        plt.plot(xvals[[0,-1]],[yval,yval],color=GRIDCOLOR)
    for xval in xvals:
        plt.plot([xval,xval],yvals[[0,-1]],color=GRIDCOLOR)
    plt.hold(holdStatus)
'''

'''
nRows=3;nCols=2
if 1:
'''
