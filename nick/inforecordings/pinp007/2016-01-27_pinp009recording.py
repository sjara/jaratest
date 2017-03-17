'''

Recording from middle of thalamus well.


941um - spikes on TT4 that are responsive to the flashlight


tons of spiking activity around 1100-1200um



lots of spikes around 1600um


'''

from jaratoolbox.test.nick.database import cellDB


rd = cellDB.Experiment('pinp009', '2016-01-27', experimenter='nick', defaultParadigm='am_tuning_curve')
site1 = rd.add_site(depth = 2935, tetrodes=[6])
site1.add_session('13-22-56', 'nb1', 'noiseburst') # Excellent sound response
site1.add_session('13-26-20', 'lp1', 'laserpulse') # No laser response, moving on..
site1.add_session('13-38-38', 'a', 'tuningCurve') # 16 freqs at 60db
site1.add_session('13-44-58', 'b', 'AM') # Not very synchronized
site1.add_session('14-05-28', 'lp2', 'laserpulse2') #No laser response

'''

Hunting for laser response.

at 3550um the responses change drastically, large fast spikes with no more sound response

I am removing the electrodes and letting the mouse rest.
'''

'''

Cortex recording


In cortex at 709um


'''

ac = cellDB.Experiment('pinp009', '2016-01-27', experimenter='nick', defaultParadigm='am_tuning_curve')
site1 = ac.add_site(depth=707, tetrodes=[6])
site1.add_session('16-33-48', None, 'noiseburst')
site1.add_session('16-36-03', None, 'laserpulse') #0.2mW
site1.add_session('16-38-50', None, 'lasertrain') #0.2mW
site1.add_session('16-42-10', 'aca', 'AM') # Stopped after 440 trials - rate coding motha
site1.add_session('17-02-02', None, 'laserpulse2') # 
site1.add_session('17-04-24', None, 'lasertrain2') # 



site2 = ac.add_site(depth=863, tetrodes=[4, 5, 6])
site2.add_session('17-14-57', None, 'noiseburst')
site2.add_session('17-17-35', None, 'laserpulse') #0.2-0.5mW
site2.add_session('17-19-44', None, 'lasertrain') #0.2-0.5mW
site2.add_session('17-23-19', 'acb', 'AM')
site2.add_session('17-42-52', None, 'laserpulse2') #0.2-0.5mW
site2.add_session('17-45-04', None, 'lasertrain2') #0.2-0.5mW
site2.add_session('17-49-18', 'acc', 'tuningCurve') #only 60dB
site2.add_session('17-53-22', 'acd', 'tuningCurve2') #30-60dB