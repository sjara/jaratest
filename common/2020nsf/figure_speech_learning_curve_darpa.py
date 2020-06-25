'''
Plot a learning curve for speech sounds.
Based on jaratest/santiago/talks/201906_darpa/figure_learning_curve.py
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from jaratoolbox import behavioranalysis
from jaratoolbox import extraplots
#import figparams


#FIGNAME = 'leaning_curve_spectral'
#dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
#STUDY_NAME = figparams.STUDY_NAME

SAVE_FIGURE = 1
outputDir = '/tmp/'

figFilename = 'leaning_curve_spectral'
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [10,5]

fontSizeLabels = 16

CASE=0
if CASE==0:
    subject = 'bili007'
    sessions = ['20180729a','20180730a','20180731a','20180801a','20180802a','20180803a','20180804a','20180805a','20180806a','20180807a','20180808a','20180809a','20180810a','20180811a','20180812a','20180813a','20180814a','20180815a','20180816a','20180818a','20180819a','20180820a','20180821a','20180822a','20180823a','20180824a','20180825a','20180826a','20180828a','20180829a','20180830a','20180831a','20180901a','20180902a','20180904a','20180905a','20180906a','20180907a','20180908a','20180909a','20180910a','20180911a','20180912a','20180913a','20180914a','20180915a','20180916a','20180917a','20180918a','20180919a','20180920a','20180922a','20180923a','20180924a','20180925a','20180926a','20180927a','20180928a','20180929a','20180930a','20181001a','20181002a','20181003a','20181004a','20181005a','20181006a','20181007a','20181008a','20181009a','20181010a','20181011a']
    excluded = ['20180817a','20180921a']
    doesNotExist = ['20190827a','20180903a']

'''
### bili007 ###
'20180701a','20180702a','20180703a','20180704a','20180705a','20180706a','20180707a','20180708a','20180709a','20180710a','20180711a','20180712a','20180713a','20180714a','20180715a',
'20180716a','20180717a','20180718a','20180719a','20180720a','20180721a','20180722a','20180723a','20180724a','20180725a','20180726a','20180728a',
,'20181012a','20181013a','20181014a','20181015a','20181016a','20181017a','20181018a','20181019a','20181020a','20181021a','20181022a','20181023a','20181024a','20181025a','20181026a','20181028a','20181029a','20181030a'
'''    
    
bdata = behavioranalysis.load_many_sessions(subject,sessions=sessions)

nSessions = bdata['sessionID'][-1]
correct = bdata['outcome']==bdata.labels['outcome']['correct']
valid = bdata['valid'].astype(bool) & (bdata['choice']!=bdata.labels['choice']['none'])

correctEachSession = np.empty(nSessions)
validEachSession = np.empty(nSessions)
for sessionID in range(nSessions):
    trialsThisSession = bdata['sessionID']==sessionID
    correctEachSession[sessionID] = np.sum(correct[trialsThisSession])
    validEachSession[sessionID] = np.sum(valid[trialsThisSession])
    ###print('{} : {}'.format(sessions[sessionID],correctEachSession[sessionID]/validEachSession[sessionID]))
    
fractionCorrect = correctEachSession/validEachSession


fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(1, 1)
gs.update(left=0.15, right=0.97, top=0.9, bottom=0.12)

ax1 = plt.subplot(gs[0])

plotColor = [0,0.4,0.7]
plt.plot(fractionCorrect,'.-',color=plotColor,lw=2,ms=16)
#plt.ylim([0.55,0.75])
plt.xlim([-1,len(sessions)])
plt.ylabel('Fraction correct',fontsize=fontSizeLabels)
plt.xlabel('Session',fontsize=fontSizeLabels)
plt.grid(True)
plt.title(subject)
plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
