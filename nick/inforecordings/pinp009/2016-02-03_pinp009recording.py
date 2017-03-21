from jaratoolbox.test.nick.database import cellDB

'''Recording from thalamus with dii on the electrodes. There are some channels that look
like they are fused. 

On TT5, channels 0 and 1 look fused
on TT6, channels 0 and 2 look fused

'''

thal=cellDB.Experiment()

site1 = thal.add_site(depth=3454, tetrodes=[ 6])
site1.add_session('12-54-32', None, 'noiseburst')# Onset responses only
site1.add_session('12-57-25', None, 'laserpulse')#1.5mW
site1.add_session('13-00-05', 'a', 'AM')#interesting tuning, possible tuning
site1.add_session('13-26-17', 'b', 'tuningCurve')#60db only

site2 = thal.add_site(depth=3603, tetrodes=[ 6])
site2.add_session('13-35-39', 'c', 'AM')
site2.add_session('13-56-00', 'd', 'tuningCurve')#60dB obly

site3 = thal.add_site(depth=3902, tetrodes=[4, 5, 6])
site3.add_session('14-12-11', None, 'noisebursts')#Good sound responses - 4 is funky
site3.add_session('14-14-59', None, 'laserpulse')
site3.add_session('14-17-26', None, 'lasertrain')#Some direct activation
site3.add_session('14-20-50', 'e', 'AM')
site3.add_session('14-41-15', None, 'laserpulse2')
site3.add_session('14-43-25', None, 'lasertrain2')
site3.add_session('14-47-05','f', 'tuningCurve')#Full TC

site4 = thal.add_site(depth=3939, tetrodes=[4, 5, 6])
site4.add_session('15-20-53', None, 'noisebursts')#
site4.add_session('15-23-16', None, 'laserpulse')#
#Moved a bit to get better sound responses on TT5, which is the only laser responsive TT right now. 

site5 = thal.add_site(depth=3959, tetrodes=[4, 5, 6])
site5.add_session('15-48-09', None, 'noisebursts')#
site5.add_session('15-51-18', None, 'laserpulse')#
site5.add_session('15-53-34', None, 'lasertrain')#
site5.add_session('15-57-54', 'g', 'AM')#
site5.add_session('16-21-49', None, 'laserpulse2')#
site5.add_session('16-24-18', None, 'lasertrain2')#

site6 = thal.add_site(depth=4005, tetrodes=[4, 5, 6])
site6.add_session('16-31-33', None, 'noisebursts')#
site6.add_session('16-33-53', None, 'laserpulse')#
site6.add_session('16-36-12', None, 'lasertrain')#
site6.add_session('16-39-28', 'h', 'AM')#
site6.add_session('17-03-34',None, 'laserpulse2')#

'''
I have gone as far as I can go, I have to take the electrodes out and do cortex tomorrow
'''