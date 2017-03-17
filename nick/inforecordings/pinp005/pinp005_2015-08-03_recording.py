'''

'''


impedences = {
3: [346, 360, 498, 379], 
4: [260, 432, 431, 423], 
5: [167, 406, 376, 422], 
6: [372, 227, 430, 429]}


laser_calib = {
    1: 1.8,
    1.5: 1.9,
    2: 2.10,
    2.5: 2.3,
    3: 2.5, 
    3.5: 2.65}

'''
1629hrs - mouse is on the rig with the electrodes in the Right thalamus well. I am trying to go a bit more medial and anterior than last time. 

977um - clear visual responses. 

At 2000um there is a lot of activity (hippocampus probably)


'''

rd = database.Experiment('pinp005', '2015-08-03', 'nick', 'laser_tuning_curve')

site1 = rd.add_site(depth= 3202, tetrodes=[4])
site1.add_session('16-46-20', none, 'nb')
site1.add_session('16-49-07', none, 'lp') #Long-latency response on T4, going to keep moving


site2 = rd.add_site(depth = 3301, tetrodes = [])
site2.add_session('16-53-44', None, 'nb') #Weak noise response (65 trials only though)
site2.add_session('16-55-18', None, 'lp') #Still a response with a latency of about 80-100msec. 

site3 = rd.add_site(depth=3500, tetrodes=[4])

site3.add_session('17-18-46', None, 'nb')
site3.add_session('17-21-20', None, 'lp')
site3.add_session('17-24-58', None, 'lt')
site3.add_session('17-28-54', 'b', 'tc')


site4 = rd.add_site(depth=3600, tetrodes=[ 3, 4, 5, 6 ])

site4.add_session('17-42-30', None, 'nb')
site4.add_session('17-44-40', None, 'lp')
site4.add_session('17-47-16', None, 'lt')
site4.add_session('17-51-47', 'c', 'tc')

site5 = rd.add_session(depth=3687, tetrodes= [3, 4, 5, 6])

site5.add_session('18-18-54', None, 'nb')
site5.add_session('18-21-31', None, 'lp')

site6 = rd.add_site(depth=3800, tetrodes=[3, 4, 5, 6]) #Good cells on T4

site6.add_session('18-30-14', None, 'nb')
site6.add_session('18-32-30', None, 'lp') #The cells on T4 look good but do not seem to respond to the laser at all.  
site6.add_session('18-34-55', None, 'lt')
site6.add_session('18-39-39', 'd', 'tc')


site7 = rd.add_site(depth= 3898, tetrodes=[3, 4, 5, 6])

site7.add_session('18-53-50', None, 'nb') #Great looking cells on TT4 again. 
#All the sessions leading up to this point were accidentally recorded with the laser at 3.5mW.

site7.add_session('18-57-10', None, 'lp') #No laser responses. Moving to a new site.


site8 = rd.add_site(depth= 4000, tetrodes=[3, 4, 5, 6])
site7.add_session('19-04-09', None, 'nb') #Responses on TT4 and 5
site7.add_session('19-06-14', None, 'lp') #No responses.

'''
1910hrs - I am removing the tetrodes and calling it a day.
'''


19-13-16 - Visual cortex, 1000um, laser pulses

19-16-40 - Visual cortex, 500um, laser pulses. 

