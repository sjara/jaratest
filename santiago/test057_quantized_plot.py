'''
Test plot where many samples are plotted at quantized levels.
'''

from jaratoolbox import extraplots
reload(extraplots)
from matplotlib import pyplot as plt
import numpy as np


plt.clf()
plt.hold(True)

y = np.array([1,2,2,2,3,3,4,4,4,4,4,6,6])
x = 0

hp = extraplots.spread_plot(x,y,spacing=0.03)
plt.setp(hp, mec='r', mew=2)

'''
possibleOffsetsOdd = 0.05*np.array([0,-1,1,-2,2,-3,3])
possibleOffsetsEven = 0.05*np.array([-0.5,0.5,-1.5,1.5,-2.5,2.5])

spacing = 0.03
uniqueY = np.unique(y)
for oneY in uniqueY:
    nVals = np.sum(y==oneY)
    #possibleOffsets = possibleOffsetsOdd if nVals%2 else possibleOffsetsEven
    possibleOffsets = spacing * np.arange(-nVals/2.0+0.5, nVals/2.0, 1)
    """
    if nVals%2:
        possibleOffsets = spacing * np.arange(-nVals/2.0+0.5, nVals/2.0, 1)
    else:
        possibleOffsets = spacing *
    """
    xOffset = possibleOffsets[:nVals]
    plt.plot(np.tile(x,nVals)+xOffset, np.tile(oneY,nVals), 'o', mec='r', mfc='none')
    #print nVals
'''

plt.ylim([0,10])
plt.xlim([-2,2])
#plt.grid(True)
plt.show()





'''
plt.bar([1,2],[4,5], align='center', fc='0.5')

xRange = [1,2]
yPos = 6
yLength = 0.5
#extraplots.significance_stars(xRange, yPos, yLength, color='k', starMarker='*', starSize=10, gapFactor=0.1)
extraplots.significance_stars(xRange, yPos, yLength, color='k', starString='n.s.', starSize=14, gapFactor=0.1)
#extraplots.new_significance_stars(xRange, yPos, yLength, color='k', starMarker='n.s.', fontSize=10, gapFactor=0.1, ax=None)
plt.ylim([0,10])
plt.show()
'''
