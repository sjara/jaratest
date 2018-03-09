import numpy as np
from matplotlib import pyplot as plt


tissueDiameters = np.array([2, 4]) #In mm
tissueVols = (4/3.0)*np.pi*(tissueDiameters/2)**3
injectionVols = np.array([200, 1000]) #In ul

# dy = np.diff(tissueVols)
# dx = np.diff(injectionVols)

# dy = tissueVols[0]
# dx = injectionVols[0]

dy = tissueVols[1]
dx = injectionVols[1]

#Force the intercept to be 0 so we don't underestimate the spread
intercept=0

xVals = np.linspace(0, 1000, 5000)
yVals = xVals*(dy/dx)

ourX = 45
ourY = ourX*(dy/dx)

plt.clf()
plt.plot(injectionVols, tissueVols, 'o')
plt.plot(xVals, yVals, '-')
plt.plot(ourX, ourY, 'ro')
plt.

ourRadius = ((3*ourY)/(4.*np.pi))**(1/3.)
print "Diameter of our injection spread: {}mm".format(ourRadius*2)
