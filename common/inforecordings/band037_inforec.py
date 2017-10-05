from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'band036'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2017-09-22', 'right_AC', info=['medialDiI','TT1ant'])
experiments.append(exp0)

exp0.laserCalibration = {
    '0.5':1.4,
    '1.0':1.8,
    '1.5':2.3,
    '2.0':2.9,
    '2.5':3.5,
    '3.0':4.1,
    '3.5':4.8
}
