'''
Fitting bandwidth tuning data.
'''


def response_curve_fit(stimArray, responseArray, type='gaussian'):
    #find best fit for frequency or bandwidth (or others) spike data
    from scipy.optimize import curve_fit
    #logStimArray = np.log2(stimArray)
    maxInd = np.argmax(responseArray)
    try:
        if type=='gaussian':
            p0 = [stimArray[maxInd], responseArray[maxInd], 1.,0.]
            curveFit = curve_fit(gaussian, stimArray, responseArray, p0=p0, maxfev=10000)[0]
        elif type=='quadratic':
            curveFit = curve_fit(quadratic, stimArray, responseArray, p0=p0, maxfev=10000)[0]
    except RuntimeError:
        print "Could not fit {} curve to tuning data.".format(type)
        return None, None, None

    #estimate best frequency and calculate R^2 value for fit
    if type=='gaussian':
        bestFreq = 2**curveFit[0]
        fitResponseArray = gaussian(stimArray, curveFit[0], curveFit[1], curveFit[2], curveFit[3])
    elif type=='quadratic':
        bestFreq = curveFit[2]/(2*curveFit[1])
        fitResponseArray = quadratic(stimArray, curveFit[0], curveFit[1], curveFit[2])
    residuals = responseArray - fitResponseArray
    SSresidual = np.sum(residuals**2)
    SStotal = np.sum((responseArray-np.mean(responseArray))**2)
    Rsquared = 1-(SSresidual/SStotal)

    return curveFit, bestFreq, Rsquared

def gaussian(x, mu, amp, sigma, offset):
    p = [mu, amp, sigma, offset]
    return p[3]+p[1]* np.exp(-((x-p[0])/p[2])**2)

def quadratic(x, a, b, c):
    return a*(x**2)+b*x+c
