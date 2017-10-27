
### THIS IS FOR PLOTTING ALL CELLS BY THEIR MAX SYNC FREQ
def mkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

soundResponsive = db.query('isiViolations<0.02 and shapeQuality>2 and noisePval<0.05')
# thal1 = soundResponsive.groupby('brainarea').get_group('rightThal')
# thal2 = soundResponsive.groupby('brainarea').get_group('rightThalamus')
# thal = pd.concat([thal1, thal2])
# ac = soundResponsive.groupby('brainarea').get_group('rightAC')
plotOnlyIdentified = False

if plotOnlyIdentified:
    baseDir = '/home/nick/data/reports/nick/2018thstr_am_sync_onlyID/'
    soundLaserResponsive = soundResponsive.query('pulsePval<0.05 and trainRatio>0.8')
    thal1 = soundLaserResponsive.groupby('brainarea').get_group('rightThal')
    thal2 = soundLaserResponsive.groupby('brainarea').get_group('rightThalamus')
    thal = pd.concat([thal1, thal2])
    ac = soundLaserResponsive.groupby('brainarea').get_group('rightAC')
else:
    baseDir = '/home/nick/data/reports/nick/2018thstr_am_sync/'
    thal1 = soundResponsive.groupby('brainarea').get_group('rightThal')
    thal2 = soundResponsive.groupby('brainarea').get_group('rightThalamus')
    thal = pd.concat([thal1, thal2])
    ac = soundResponsive.groupby('brainarea').get_group('rightAC')

astrR = soundResponsive.groupby('brainarea').get_group('rightAstr')
astrL = soundResponsive.groupby('brainarea').get_group('rightAstr')
astr = pd.concat([astrR, astrL])

thalDir = os.path.join(baseDir, 'thalamus')
acDir = os.path.join(baseDir, 'ac')
astrDir = os.path.join(baseDir, 'astr')
mkdir(baseDir)

#Thalamus
mkdir(thalDir)
# for indCell, cell in thal.iterrows():
for rate in np.unique(thal['highestSync']):
    thisRateDir = os.path.join(thalDir, '{}'.format(np.round(rate, 0)))
    mkdir(thisRateDir)
    cellsThisRate = thal[thal['highestSync']==rate]
    for indCell, cell in cellsThisRate.iterrows():
        savePath = os.path.join(thisRateDir, 'cell{}.png'.format(indCell))
        # am_example(cell, timeRange=[0.1, 0.5])
        am_example(cell)
        plt.savefig(savePath)

#AC
mkdir(acDir)
# for indCell, cell in thal.iterrows():
for rate in np.unique(ac['highestSync']):
    thisRateDir = os.path.join(acDir, '{}'.format(np.round(rate, 0)))
    mkdir(thisRateDir)
    cellsThisRate = ac[ac['highestSync']==rate]
    for indCell, cell in cellsThisRate.iterrows():
        savePath = os.path.join(thisRateDir, 'cell{}.png'.format(indCell))
        # am_example(cell, timeRange=[0.1, 0.5])
        am_example(cell)
        plt.savefig(savePath)

#AStr
mkdir(astrDir)
for rate in np.unique(astr['highestSync']):
    thisRateDir = os.path.join(astrDir, '{}'.format(np.round(rate, 0)))
    mkdir(thisRateDir)
    cellsThisRate = astr[astr['highestSync']==rate]
    for indCell, cell in cellsThisRate.iterrows():
        savePath = os.path.join(thisRateDir, 'cell{}.png'.format(indCell))
        # am_example(cell, timeRange=[0.1, 0.5])
        am_example(cell)
        plt.savefig(savePath)
