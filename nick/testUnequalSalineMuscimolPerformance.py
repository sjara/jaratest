from pylab import *
from jaratoolbox import loadbehavior
from jaratoolbox.test.nick import behavioranalysis_vnick as behavioranalysis
reload(behavioranalysis)

animal = 'amod003'


# salineSessions = ['20160412a', '20160414a']

# muscimolSessions = ['20160413a', '20160415a', '20160417a']

salineSessions = ['20160412a', '20160414a', '20160416a', '20160418a', '20160420a']

muscimolSessions = ['20160413a', '20160415a', '20160417a', '20160419a', '20160421a','20160422a', '20160423a', '20160424a']


plotCols = 4
# plotRows = len(muscimolSessions)
plotRows = max(len(muscimolSessions), len(salineSessions))

clf()

# 2 sound types, muscimol/saline
for indRow in range(len(salineSessions)):

    #Plot chords saline
    subplot(plotRows, plotCols, indRow*4+1)

    soundType = 'chords'

    date = salineSessions[indRow]
    fn = '/home/nick/data/behavior/nick/{0}/{1}_2afc_{2}.h5'.format(animal, animal, date)
    #fn = '/var/tmp/data/santiago/nick/nick_2afc_20160330a.h5' #Not psycurve
    bdata = loadbehavior.BehaviorData(fn)
    behavioranalysis.plot_frequency_psycurve_soundtype(bdata, soundType)
    title('{} {}'.format(date, soundType))
    xlabel('')

    subplot(plotRows, plotCols, indRow*4+2)

    soundType = 'amp_mod'

    date = salineSessions[indRow]
    fn = '/home/nick/data/behavior/nick/{0}/{1}_2afc_{2}.h5'.format(animal, animal, date)
    #fn = '/var/tmp/data/santiago/nick/nick_2afc_20160330a.h5' #Not psycurve
    bdata = loadbehavior.BehaviorData(fn)
    behavioranalysis.plot_frequency_psycurve_soundtype(bdata, soundType)
    title('{} {}'.format(date, soundType))
    xlabel('')



for indRow in range(len(muscimolSessions)):

    #plot mod saline
    subplot(plotRows, plotCols, indRow*4+3)
    soundType = 'amp_mod'

    date = muscimolSessions[indRow]
    fn = '/home/nick/data/behavior/nick/{0}/{1}_2afc_{2}.h5'.format(animal, animal, date)
    #fn = '/var/tmp/data/santiago/nick/nick_2afc_20160330a.h5' #Not psycurve
    bdata = loadbehavior.BehaviorData(fn)
    behavioranalysis.plot_frequency_psycurve_soundtype(bdata, soundType)
    title('{} {}'.format(date, soundType))

    soundType = 'chords'


    # plot mod muscimol
    subplot(plotRows, plotCols, indRow*4+4)

    date = muscimolSessions[indRow]
    fn = '/home/nick/data/behavior/nick/{0}/{1}_2afc_{2}.h5'.format(animal, animal, date)
    #fn = '/var/tmp/data/santiago/nick/nick_2afc_20160330a.h5' #Not psycurve
    bdata = loadbehavior.BehaviorData(fn)
    behavioranalysis.plot_frequency_psycurve_soundtype(bdata, soundType)
    title('{} {}'.format(date, soundType))
    xlabel('')


    xlabel('')

# suptitle('saline        -        muscimol          -           saline         -         muscimol')

show()
