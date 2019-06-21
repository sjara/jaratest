''' Based on Yashar's code taken from https://github.com/ahmadianlab/ACbandwidth/blob/master/tuning_curve_fit_funcs.py

This module contains the functions used to fit the difference of Gaussians form for our bandwidth tuning curves.'''

import numpy as np
from scipy.special import erf
import time



def diff_gauss_form(x, mExp, R0, sigmaD, sigmaS, RD, RS):
    '''The difference of Gaussians form for Bandwidth tuning curve, inspired by "subtractive normalization."'''
    return R0 + RD* (erf(x/(np.sqrt(2)*sigmaD)))**mExp - RS* erf(x/(np.sqrt(2)*sigmaS))**mExp


def diff_of_gauss_fit(stimuli, responses, RFscale = None, mFixed=None):
    '''Find best fit of difference of gaussians model (really diff of erf's) to bandwidth tuning curve of one cell using least squares.
    
    Inputs:
        stimuli: array of floats corresponding to stimulus presented each trial
        responses: array of floats corresponding to firing rate during each trial
        RFscale: ?
        mFixed: float, what the m exponent will be fixed to in the difference of gaussian form, or None is m is a parameter to be fit, defaults to None
        
    Outputs:
        fitParams: array of parameters of best difference of Gaussians fit
        R2: R squared value for fit'''
    from scipy.optimize import curve_fit

    if RFscale is None:
        RFscale = stimuli[2] # = stimuli[np.argmax(responses)] # = summation field size
    MaxResp = np.max(np.abs(responses))
    MaxNegResp = np.max(-responses)
    if MaxNegResp < 0:
        MaxNegResp = 0

    #set up Lower and Upper bounds on Parameters
    maxM = 10
    maxsigD = 3*np.max(stimuli) #3* np.max(stimuli) #max(xs)/2
    maxsigS = 3*np.max(stimuli) #4* np.max(stimuli)
    maxRD = 2* MaxResp+1 #10* MaxResp
    maxR0 = 3*responses[0]+1
    Upper = np.asarray([maxM , maxR0, maxsigD ,maxsigS , maxRD, maxRD])
    Lower= np.asarray([1 , 0, RFscale/100., RFscale/100., 0 ,  0])

    #set up different initialization sets for parameters
    Nparsets = 5
    initpars = np.asarray([[2.5, responses[0], RFscale, 2*RFscale, MaxResp, MaxNegResp]]).T * np.ones((6,Nparsets)) #uses broadcasting. This gives error (shape mismatch for broadcasting): initpars = np.ones((5,Nparsets)) * np.asarray([2.5, RFscale, 2*RFscale, MaxResp, 1])
    #                      [m  , sigmaD , sigmaS   , RD    , RS ]
    p = 0
    initpars[4,p] *= .5
    p += 1
    initpars[0,p] = 2.0 # m
    initpars[5,p] = 0.01 # RS
    p += 1
    initpars[0,p] = 2.0 # m
    initpars[4,p] *= 2 # RD
    initpars[5,p] *= 2 # RS
    p += 1
    initpars[0,p] = 3.0 # m
    initpars[2,p] = 4*RFscale # sigmaD
    initpars[3,p] = RFscale # sigmaS

    curve_form = diff_gauss_form
    if mFixed is not None:
        Upper = Upper[1:]
        Lower = Lower[1:]
        initpars = initpars[1:,:]
        curve_form = lambda x, R0, sigmaD, sigmaS, RD, RS: diff_gauss_form(x, mFixed, R0, sigmaD, sigmaS, RD, RS)#diff_gauss_form_fixed_m

    fitParams = None
    fitResponses = None
    SSE = np.inf
    for p in range(Nparsets):
        try:
            fitParams0 = curve_fit(curve_form, stimuli, responses, p0=initpars[:,p], bounds = (Lower,Upper), max_nfev=10000)[0]
            fitResponses0 = curve_form(stimuli, *fitParams0)
            SqErr = np.sum((responses - fitResponses0)**2)
            if SqErr < SSE:
                fitParams = fitParams0
                fitResponses = fitResponses0
                SSE = SqErr

        except RuntimeError:
            print("Could not fit {} curve to tuning data with the {}-th initialization set.".format('Difference of Gaussian',p))
            
    SStotal = np.sum((responses-np.mean(responses))**2)
    R2 = 1-(SSE/SStotal)

    return fitParams, R2 #, fitResponses


def extract_stats_from_fit(fitParams, testStims):
    '''Calculate tuning curve features using the given best fit difference-of-Gaussians-form
    
    Inputs:
        fitParams: array of floats containing parameters of difference of gaussian fit
        testStims: array of floats containing test stimuli used to calculate tuning curve
        
    Outputs:
        suppInd: suppression index of fit bandwidth tuning curve
        prefBW: preferred bandwidth of fit bandwidth tuning curve'''

    testResps = diff_gauss_form(testStims, *fitParams)
    prefBW = testStims[np.argmax(testResps)]
    suppInd = 1 - testResps[-1]/np.max(testResps)

    return suppInd, prefBW