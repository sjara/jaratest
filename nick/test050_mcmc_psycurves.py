from jaratoolbox.test.nick import behavioranalysis_vnick as behavioranalysis
import pymc as pm


def logistic(xval,alpha,beta):
    return 1/(1+np.exp(-(xval-alpha)/beta))

def psychfun(xval,alpha,beta,lamb,gamma):
    '''Psychometric function that allowing arbitrary asymptotes.
    alpha: bias
    beta : related to slope
    lamb : lapse term (up)
    gamma: lapse term (down)
    '''
    #return gamma + (1-gamma-lamb)*weibull(xval,alpha,beta)
    #return gamma + (1-gamma-lamb)*gaussianCDF(xval,alpha,beta)
    return gamma + (1-gamma-lamb)*logistic(xval,alpha,beta)

# priors for params used now:
# constraints = ( 'Uniform({}, {})'.format(lowerFreqConstraint, upperFreqConstraint), 'Uniform(0,5)' ,'Uniform(0,0.5)', 'Uniform(0,0.5)')

# some data


# animals = ['adap023', 'adap022', 'adap026', 'adap027', 'adap030']
animals = ['adap023']
salineSessions = {'adap023': ['20160428a', '20160430a', '20160502a', '20160504b', '20160506a', '20160508a'],
                  'adap022': ['20160531a', '20160602a', '20160606a', '20160608a', '20160610a'],
                  'adap026': ['20160531a', '20160602a', '20160606a', '20160608a', '20160610a'],
                  'adap027': ['20160531a', '20160602a', '20160606a', '20160608a', '20160610a'],
                  'adap030': ['20160531a', '20160602a', '20160606a', '20160608a', '20160610a']
}

muscimolSessions = {'adap023': ['20160429a', '20160501a', '20160503a', '20160505a', '20160507a', '20160509a'],
                   'adap022': ['20160601a', '20160603a', '20160607a', '20160609a', '20160611a'],
                   'adap026': ['20160601a', '20160603a', '20160607a', '20160609a', '20160611a'],
                   'adap027': ['20160601a', '20160603a', '20160607a', '20160609a', '20160611a'],
                   'adap030': ['20160601a', '20160603a', '20160607a', '20160609a', '20160611a']
}

mdata = behavioranalysis.load_many_sessions(animal, muscimolSessions[animal])
sdata = behavioranalysis.load_many_sessions(animal, salineSessions[animal])

bdata = sdata
freqEachTrial = bdata['targetFrequency']

possibleFreq = np.unique(freqEachTrial)
lowerFreqConstraint = possibleFreq[1]
upperFreqConstraint = possibleFreq[-2]



alpha = pm.Uniform('alpha', lowerFreqConstraint, upperFreqConstraint)



