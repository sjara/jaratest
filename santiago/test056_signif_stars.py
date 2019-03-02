'''
Test significant stars from extraplots.
'''

from jaratoolbox import extraplots
reload(extraplots)
from matplotlib import pyplot as plt

plt.clf()
plt.bar([1,2],[4,5], align='center', fc='0.5')

xRange = [1,2]
yPos = 6
yLength = 0.5
#extraplots.significance_stars(xRange, yPos, yLength, color='k', starMarker='*', starSize=10, gapFactor=0.1)
extraplots.significance_stars(xRange, yPos, yLength, color='k', starString='n.s.', starSize=14, gapFactor=0.1)
#extraplots.new_significance_stars(xRange, yPos, yLength, color='k', starMarker='n.s.', fontSize=10, gapFactor=0.1, ax=None)
plt.ylim([0,10])

plt.show()
