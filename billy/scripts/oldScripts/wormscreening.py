'''
wormscreening.py
author: Billy Walker
'''

import matplotlib.pyplot as plt
from math import log10


regWormFrac = 0.05 #fraction of nonsignificantly mutanted worms chose M over G
mutWormFrac = 0.5 #fraction of significantly mutanted worms chose M over G
mutPercent = 1.0/10000.0 #fraction of worms that are significantly mutated
wormScreeningRate = 1.0 #number of worms per second being screened


plotRangeLayers = range(0,9)
numLayer = 4 #number of layers or choices in screening between M and G
finalMutPercent = 1000 #percentage/likelihood worm being a mutant after passing through screening

finalFrac=[0]*len(plotRangeLayers)

for layer,indLayer in enumerate(plotRangeLayers):
    finalFrac[indLayer] = mutPercent*(mutWormFrac/regWormFrac)**layer

plt.clf()
plt.plot(plotRangeLayers,finalFrac)
plt.show()

finalFrac_numLayer = mutPercent*(mutWormFrac/regWormFrac)**numLayer
numLayerNeeded = log10(finalMutPercent/mutPercent)/log10(mutWormFrac/regWormFrac)
totalWormScreen = 1.0/(mutPercent*(mutWormFrac**numLayer))
totalScreenTime = totalWormScreen/wormScreeningRate
totalScreenTimeHour = totalScreenTime/60.0
totalScreenTimeDay = totalScreenTimeHour/24.0

print 'With {} layers, the final fraction of significantly mutated worms is {}'.format(numLayer,finalFrac_numLayer)

print 'To get a final fraction of significantly mutated worms of {}, the number of layers needed is {}'.format(finalMutPercent,numLayerNeeded)

print 'The number of worms needed to be checked before finding one mutant is {}'.format(totalWormScreen)

print 'The total time it will take to find one signifcantly mutated worm is {}sec, or {}hours, or {}days'.format(totalScreenTime,totalScreenTimeHour,totalScreenTimeDay)
