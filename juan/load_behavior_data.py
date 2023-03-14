from jaratoolbox import loadbehavior
import matplotlib.pyplot as plt

subject = "coop010x011"  # The name of the mouse
paradigm = "coop4ports"  # The paradigm name is also part of the data file name
session = "20230313a"  # The format is usually YYYYMMDD and a short suffix
behavFile = loadbehavior.path_to_behavior_data(subject, paradigm, session)
bdata = loadbehavior.BehaviorData(behavFile)

##  I WANT TO IDENTIFY IF IT EXISTS A POINT OF TIME WITH THE MAJOR ACTIVITY
mask = bdata ['outcome'] == 1
bdata['outcome'][mask]
bdata['timeTrialStart'] [mask]

plt.plot(bdata['timeTrialStart'] [mask], bdata['outcome'][mask], marker='o')
plt.show()