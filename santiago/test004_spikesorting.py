'''
Example of using spikesorting module (which uses KlustaKwik) for spike sorting
'''

from jaratoolbox import spikesorting
reload(spikesorting)

CASE = 2

if CASE==1:
    animalName = 'test030'
    ephysSession = '2014-06-25_18-33-30_TT6goodGND'
    tetrodes = [6]
if CASE==2:
    animalName = 'pinp001'
    #ephysSession = '2015-03-21_23-56-20'  # sound
    #ephysSession = '2015-03-22_00-02-54'  # laser
    #ephysSession = '2015-03-22_00-12-18'  # tuning
    #ephysSession = '2015-03-22_17-13-54'  # tuning
    #ephysSession = '2015-03-22_17-27-28'  # laser
    #ephysSession = '2015-03-22_17-40-55'  # tuning (4-20)
    #ephysSession = '2015-03-23_21-51-50' # tuning (2-30)
    #ephysSession = '2015-03-23_22-33-20'  # laser
    ephysSession = '2015-03-23_22-46-13' # tuning (2-30)
    ephysSession = '2015-03-23_23-04-21'  # laser
    ephysSession = '2015-03-23_23-23-10'  # laser train


    tetrodes = [3,4,5,6]

for tetrode in tetrodes:
    oneTT = spikesorting.TetrodeToCluster(animalName,ephysSession,tetrode)
    oneTT.create_fet_files()  # This runs oneTT.load_waveforms()
    oneTT.run_clustering()
    oneTT.save_report()
