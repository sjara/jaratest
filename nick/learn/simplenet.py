#Simple 2-layer neural network

import numpy as np

def nonlin(x, deriv=False):
    if deriv:
        return x*(1-x)
    else:
        return 1/(1+np.exp(-x))

X = np.array([ [0, 0, 1],
               [0, 1, 1],
               [1, 0, 1],
               [1, 1, 1]])

y = np.array([[0, 0, 1, 1]]).T

np.random.seed(1)

syn0 = 2*np.random.random((3, 1))-1

for step in xrange(10000):

    #forward propagation

    l0 = X
    l1 = nonlin(np.dot(l0, syn0))

    #how much did we miss?
    l1Error = y-l1

    #multiply how much we missed by the slope of the
    #sigmoid at the values in l1

    l1Delta = l1Error * nonlin(l1, deriv=True)

    #update the weights
    syn0 += np.dot(l0.T, l1Delta)

print "Output after training"
print l1

