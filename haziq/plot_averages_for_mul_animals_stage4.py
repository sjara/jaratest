
"""
Plot psychmetric curve for an animal trained with the fm_discrimination paradigm.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import statistics as st
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import extraplots

subject = ['pamo009', 'pamo010', 'pamo011', 'pamo012',
           'pamo013', 'pamo014', 'pamo015', 'pamo016',
           'pamo017', 'pamo018', 'pamo019', 'pamo020',
           'pamo021', 'pamo022', 'pamo023', 'pamo024',
           'pamo025', 'pamo026']
paradigm = '2afc'
J009 = ['20220324a','20220323a','20220322a','20220321a',
      '20220320a','20220319a','20220318a','20220317a',
      '20220316a','20220315a','20220314a','20220313a',
      '20220312a','20220311a','20220310a','20220309a',
      '20220308a','20220307a','20220306a','20220305a',
      '20220304a','20220303a','20220302a','20220301a',
      '20220228a']
J010 = ['20220324a','20220323a','20220322a','20220321a',
      '20220320a','20220319a','20220318a','20220317a',
      '20220316a','20220315a','20220314a','20220313a',
      '20220312a','20220311a','20220310a','20220309a',
      '20220308a','20220307a','20220306a','20220305a',
      '20220304a','20220303a','20220302a','20220301a',
      '20220228a']
J011 = ['20220324a','20220323a','20220322a','20220321a',
      '20220320a','20220319a','20220318a','20220317a',
      '20220316a','20220315a','20220314a','20220313a',
      '20220312a','20220311a','20220310a','20220309a',
      '20220308a','20220307a','20220306a','20220305a',
      '20220304a','20220303a','20220302a','20220301a',
      '20220228a']
J012 = ['20220324a','20220323a','20220322a','20220321a',
      '20220320a','20220319a','20220318a','20220317a',
      '20220316a','20220315a','20220314a','20220313a',
      '20220312a','20220311a','20220310a','20220309a',
      '20220308a','20220307a','20220306a','20220305a',
      '20220304a','20220303a','20220302a','20220301a',
      '20220228a']
J013 = ['20220324a','20220323a','20220322a','20220321a',
      '20220320a','20220319a','20220318a','20220317a',
      '20220316a','20220315a','20220314a','20220313a',
      '20220312a','20220311a','20220310a','20220309a',
      '20220308a','20220307a','20220306a','20220305a',
      '20220304a','20220303a','20220302a','20220301a',
      '20220228a']
J014 = ['20220324a','20220323a','20220322a','20220321a',
      '20220320a','20220319a','20220318a','20220317a',
      '20220316a','20220315a','20220314a','20220313a',
      '20220312a','20220311a','20220310a','20220309a',
      '20220308a','20220307a','20220306a','20220305a',
      '20220304a','20220303a','20220302a','20220301a',
      '20220228a']
J015 = ['20220324a','20220323a','20220322a','20220321a',
      '20220320a','20220319a','20220318a','20220317a',
      '20220316a','20220315a','20220314a','20220313a',
      '20220312a','20220311a','20220310a','20220309a',
      '20220308a','20220307a','20220306a','20220305a',
      '20220304a','20220303a','20220302a','20220301a',
      '20220228a']
J016 = ['20220324a','20220323a','20220322a','20220321a',
      '20220320a','20220319a','20220318a','20220317a',
      '20220316a','20220315a','20220314a','20220313a',
      '20220312a','20220311a','20220310a','20220309a',
      '20220308a','20220307a','20220306a','20220305a',
      '20220304a','20220303a','20220302a','20220301a']
J017 = ['20220324a','20220323a','20220322a','20220321a',
      '20220320a','20220319a','20220318a','20220317a',
      '20220316a','20220315a','20220314a','20220313a',
      '20220312a','20220311a','20220310a','20220309a',
      '20220308a','20220307a','20220306a','20220305a',
      '20220304a','20220303a','20220302a','20220301a',
      '20220228a']
J018 = ['20220324a','20220323a','20220322a','20220321a',
      '20220320a','20220319a','20220318a','20220317a',
      '20220316a','20220315a','20220314a','20220313a',
      '20220312a','20220311a','20220310a','20220309a',
      '20220308a','20220307a','20220306a','20220305a',
      '20220304a','20220303a','20220302a','20220301a']
J019 = ['20220324a','20220323a']
J020 = ['20220324a','20220323a','20220322a','20220321a',
      '20220320a','20220319a','20220318a','20220317a',
      '20220316a','20220315a','20220314a','20220313a',
      '20220312a','20220311a','20220310a','20220309a',
      '20220308a','20220307a','20220306a','20220305a',
      '20220304a','20220303a','20220302a','20220301a',
      '20220228a']
J021 = ['20220324a','20220323a','20220322a','20220321a',
      '20220320a','20220319a','20220318a','20220317a',
      '20220316a','20220315a','20220314a','20220313a',
      '20220312a','20220311a','20220310a','20220309a',
      '20220308a','20220307a','20220306a','20220305a',
      '20220304a','20220303a','20220302a','20220301a',
      '20220228a']
J022 = ['20220324a','20220323a','20220322a','20220321a',
      '20220320a','20220319a','20220318a','20220317a',
      '20220316a','20220315a','20220314a',
      '20220312a','20220311a','20220310a','20220309a',
      '20220308a','20220307a','20220306a','20220305a',
      '20220304a','20220303a','20220302a','20220301a',
      '20220228a']
J023 = ['20220324a','20220323a','20220322a','20220321a',
      '20220320a','20220319a','20220318a','20220317a',
      '20220316a','20220315a','20220314a','20220313a',
      '20220312a','20220311a','20220310a','20220309a',
      '20220308a','20220307a','20220306a','20220305a',
      '20220304a','20220303a','20220302a','20220301a',
      '20220228a']
J024 = ['20220324a','20220323a','20220322a','20220321a',
      '20220320a','20220319a','20220318a','20220317a',
      '20220316a','20220315a','20220314a','20220313a',
      '20220312a','20220311a','20220310a','20220309a',
      '20220308a','20220307a','20220306a','20220305a',
      '20220304a','20220303a','20220302a','20220301a',
      '20220228a']
J025 = ['20220324a','20220323a','20220322a','20220321a',
      '20220320a','20220319a','20220318a','20220317a',
      '20220316a','20220315a','20220314a','20220313a',
      '20220312a','20220311a','20220310a','20220309a',
      '20220308a','20220307a','20220306a','20220305a',
      '20220304a','20220303a','20220302a','20220301a',
      '20220228a']
J026 = ['20220324a','20220323a','20220322a','20220321a',
      '20220320a','20220319a','20220318a','20220317a',
      '20220316a','20220315a','20220314a','20220313a',
      '20220312a','20220311a','20220310a','20220309a',
      '20220308a','20220307a','20220306a','20220305a',
      '20220304a','20220303a','20220302a','20220301a',
      '20220228a']
sessions=[J009,J010,J011,J012,J013,J014,J015,J016,J017,J018,J019,J020,J021,J022,J023,J024,J025,J026]

# variables
A_only = ['pamo009', 'pamo011', 'pamo012', 'pamo013',
          'pamo016', 'pamo019', 'pamo020', 'pamo022',
          'pamo026']
AP_group = ['pamo010', 'pamo014', 'pamo015', 'pamo017',
            'pamo018', 'pamo021', 'pamo023', 'pamo024',
            'pamo025']
APgroup_perf_mul_animal = []
Agroup_perf_mul_animal = []
average_mean_AP_group = []
average_mean_A_group = []


def caluculating_averages_multipledays(subject,paradigm,sessions, Aonly):
    n=0
    for y in subject:
        #print (n)
        avg_performance = []
        #print (y)
        for x in sessions[n]:
            #print (x)
            behavFile = loadbehavior.path_to_behavior_data(y, paradigm, x)
            bdata = loadbehavior.BehaviorData(behavFile)
            correct_trials_count = np.count_nonzero(bdata['outcome'] == bdata.labels['outcome']['correct']) #no of correct trials type int
            valid_trials_count = np.count_nonzero(bdata['valid'] == True)  #no of valid trials type int    
            average_performance = (correct_trials_count/valid_trials_count)*100 # type float
            avg_performance.append(float("{:.2f}".format(average_performance))) # type list
        if y in A_only:
            Agroup_perf_mul_animal.append(avg_performance)
        else:
            APgroup_perf_mul_animal.append(avg_performance)
        n+=1
    return APgroup_perf_mul_animal, Agroup_perf_mul_animal

def calculating_mean_averages(APgroup_perf_mul_animal, Agroup_perf_mul_animal):
    for i in range(len(APgroup_perf_mul_animal)):
        average_mean_AP_group.append(float("{:.2f}".format(st.mean (APgroup_perf_mul_animal[i]))))    
        average_mean_A_group.append(float("{:.2f}".format(st.mean (Agroup_perf_mul_animal[i]))))
    return average_mean_AP_group, average_mean_A_group
#print(average_mean_AP_group)
#print(average_mean_A_group)


(APgroup_perf_mul_animal, Agroup_perf_mul_animal)=caluculating_averages_multipledays(subject, paradigm, sessions, A_only)
(average_mean_AP_group, average_mean_A_group) = calculating_mean_averages(APgroup_perf_mul_animal, Agroup_perf_mul_animal)


x = [1,2,3,4,5,6,7,8,9]
plt.subplot(1,2,1)
for xe, ye in zip(x, Agroup_perf_mul_animal):
    plt.scatter([xe] * len(ye), ye)
    plt.plot(x,average_mean_A_group, 'k_', markersize=25)
plt.ylim(40, 100)
plt.xticks(range(10), ['',A_only[0], A_only[1], A_only[2], A_only[3], A_only[4], A_only[5], A_only[6], A_only[7], A_only[8]], rotation = 90 )
plt.xlabel("Animals")
plt.ylabel("Performance in percentage")
plt.title("Active only group performance for all days at stage 4 ")
plt.grid(axis = 'y')
#print(len(x))
#print(len(Agroup_perf_mul_animal))


plt.subplot(1,2,2)
for xe, ye in zip(x, APgroup_perf_mul_animal):
    plt.scatter([xe] * len(ye), ye)
plt.plot(x,average_mean_AP_group, 'k_', markersize=25)
plt.ylim(40, 100)

plt.xticks(range(10), ['',AP_group[0], AP_group[1], AP_group[2], AP_group[3], AP_group[4], AP_group[5], AP_group[6], AP_group[7], AP_group[8]], rotation = 90 )
plt.xlabel("Animals")
plt.ylabel("Performance in percentage")
plt.title("Active + passive group performance for all days at stage 4 ")
plt.grid(axis = 'y')
plt.show()

