'''
Translate old inforec file to new.

python test047_translate_inforec.py > /tmp/newinforec.py


'''

filename = '/home/sjara/src/jaratest/lan/analysis_photostim/photostim_ephys_behav_database_good_clusters.py'
fid = open(filename,'r')
lines = fid.readlines()

replacements = [ ['session = photostim.PhotostimSession(animalName=',
                  'oneExp = celldatabase.Experiment('],
                 ['exp = photostim.PhotostimSession(animalName=',
                              'oneExp = celldatabase.Experiment('],
                 ['date =',''],
                 ["sessionTypes['nb']", "'noiseBurst'"],
                 ["sessionTypes['tc']", "'tuningCurve'"],
                 ["sessionTypes['lp']", "'laserPulse'"],
                 ["'noiseBurst'", "'noiseBurst', 'laser_tuning_curve'"],
                 ["'tuningCurve'", "'tuningCurve', 'laser_tuning_curve'"],
                 ["'laserPulse'", "'laserPulse', 'laser_tuning_curve'"],
                 ["sessionTypes['2afc']", "'2afc'"],
                 ["experimenter='', defaultParadigm='laser_tuning_curve'",
                  "brainarea='', info=''"],
                 ['site1 = session.add_site','oneExp.add_site'],
                 ['site1 = exp.add_site','oneExp.add_site'],
                 ['site1.add_session', 'oneExp.add_session'],
                 [", stimHemi='left'", ''],
                 [", stimHemi='right'", ''],
                 ["site1.add_clusters", "#site1.add_clusters"],
                 ['siteList.append(site1)',''],
                 ['site1.cluster_photostim_session()',''],
                 ]


newLines = []
for oneline in lines:
    newline = oneline
    for onereplace in replacements:
        newline = newline.replace(*onereplace)
    newLines.append(newline)

for oneline in newLines[:]:
    print oneline,

