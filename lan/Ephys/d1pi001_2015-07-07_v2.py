from jaratoolbox.test.nick.ephysExperiments import ephys_experiment_v2 as ee2
reload(ee2)

#The session types to use for this kind of experiment
#Can use a dict like this or simply write the sesison types directly
#I used this to avoid typing errors and to save time
sessionTypes = {'nb':'noiseBurst',
                'lp':'laserPulse',
                'lt':'laserTrain',
                'tc':'tuningCurve',
                'bf':'bestFreq',
                '3p':'3mWpulse',
                '1p':'1mWpulse'} 

today = ee2.RecordingDay(animalName = 'd1pi001', date = '2015-07-07', experimenter = 'lan')

site1 = ee2.RecordingSite(today, depth = 2750, goodTetrodes = [3])
site1.add_session('14-10-13', None, sessionTypes['nb'])
site1.add_session('14-11-42', None, sessionTypes['lp'])
site1.add_session('14-14-00', None, sessionTypes['lt'])
site1.add_session('14-17-54', 'a', sessionTypes['tc'])

site2 = ee2.RecordingSite(today, depth = 2900, goodTetrodes = [3])
site2.add_session('15-12-17', None, sessionTypes['nb'])
site2.add_session('15-14-12', None, sessionTypes['lp'])
site2.add_session('15-16-18', None, sessionTypes['lt'])
site2.add_session('15-18-44', 'b', sessionTypes['tc'])

site3 = ee2.RecordingSite(today, depth = 3025, goodTetrodes = [3, 6])
site3.add_session('16-04-26', None, sessionTypes['nb'])
site3.add_session('16-06-32', None, sessionTypes['lp'])
site3.add_session('16-08-28', None, sessionTypes['lt'])
site3.add_session('16-12-41', 'c', sessionTypes['tc'])


site4 = ee2.RecordingSite(today, depth = 3075, goodTetrodes = [3, 6])
site4.add_session('16-34-24', None, sessionTypes['nb'])
site4.add_session('16-36-42', None, sessionTypes['lp'])
site4.add_session('16-38-59', None, sessionTypes['lt'])
site4.add_session('16-42-17', 'd', sessionTypes['tc'])
site4.add_session('16-55-51', None, sessionTypes['1p'])
site4.add_session('16-57-40', None, sessionTypes['3p'])

site5 = ee2.RecordingSite(today, depth = 3125, goodTetrodes = [3, 6])
site5.add_session('17-02-39', None, sessionTypes['nb'])
site5.add_session('17-05-02', None, sessionTypes['lp'])
site5.add_session('17-07-13', None, sessionTypes['lt'])
site5.add_session('17-10-30', 'e', sessionTypes['tc'])
site5.add_session('17-25-32', None, sessionTypes['1p'])
site5.add_session('17-26-58', None, sessionTypes['3p'])

site6 = ee2.RecordingSite(today, depth = 3200, goodTetrodes = [3, 6])
site6.add_session('17-31-32', None, sessionTypes['nb'])
site6.add_session('17-33-53', None, sessionTypes['lp'])
site6.add_session('17-36-05', None, sessionTypes['lt'])
site6.add_session('17-39-12', 'f', sessionTypes['tc'])
site6.add_session('17-52-09', None, sessionTypes['3p'])
site6.add_session('17-54-00', None, sessionTypes['1p'])

site7 = ee2.RecordingSite(today, depth = 3275, goodTetrodes = [3,4,6])
site7.add_session('18-01-55', None, sessionTypes['nb'])
site7.add_session('18-03-53', None, sessionTypes['lp'])
site7.add_session('18-05-36', None, sessionTypes['lt'])
site7.add_session('18-08-36', 'g', sessionTypes['tc'])
site7.add_session('18-22-56', None, sessionTypes['3p'])
site7.add_session('18-24-20', None, sessionTypes['1p'])

site8 = ee2.RecordingSite(today, depth = 3325, goodTetrodes = [3,4,6])
site8.add_session('18-29-42', None, sessionTypes['nb'])
site8.add_session('18-32-16', None, sessionTypes['lp'])
site8.add_session('18-34-54', None, sessionTypes['lt'])
site8.add_session('18-42-14', 'h', sessionTypes['tc'])
site8.add_session('18-53-39', None, sessionTypes['3p'])


from jaratoolbox.test.lan.Ephys import laserTCanalysis_added_clu_report as laserTC
reload(laserTC)
for indSite, site in enumerate(today.siteList):
    laserTC.laser_tc_analysis(site, indSite+1)



