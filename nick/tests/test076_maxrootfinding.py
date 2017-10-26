from scipy import optimize
from matplotlib import pyplot as plt

def gaussian(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))

a = 5
x0 = 5
sigma = 2

x = linspace(0, 10, 100)
y = gaussian(x, a, x0, sigma)

plt.clf()
plt.plot(x, y)
plt.ylim([0, 5.5])
plt.axhline(y=2, color='k')

#Function to minimize
fm = lambda x: -gaussian(x, a, x0, sigma)
r = optimize.minimize_scalar(fm, bounds=(0, 10))
plt.plot(r["x"], gaussian(r["x"], a, x0, sigma), 'r*')

#Function to find roots for
fr = lambda x: gaussian(x, a, x0, sigma) - 2
#Lower intersection
rootLower = optimize.brentq(fr, 0, r["x"])
#Upper intersection
rootUpper  = optimize.brentq(fr, r["x"], 10)

plt.plot(rootLower, gaussian(rootLower, a, x0, sigma), 'r*')
plt.plot(rootUpper, gaussian(rootUpper, a, x0, sigma), 'r*')

plt.show()
