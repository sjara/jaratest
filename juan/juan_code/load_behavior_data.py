from jaratoolbox import loadbehavior

subject = "coop010x011"  # The name of the mouse
paradigm = "coop4ports"  # The paradigm name is also part of the data file name
session = "20230304a"  # The format is usually YYYYMMDD and a short suffix
behavFile = loadbehavior.path_to_behavior_data(subject, paradigm, session)
bdata = loadbehavior.BehaviorData(behavFile)
import matplotlib.pyplot as plt
import matplotlib.animation as animation

result_trials=bdata['outcome']
labels_outcomes=bdata.labels['outcome']

# Here I estimate the time of each trial
# Given that a fail trial last 3 seconds and successful trial 6 seconds  
waitTime= 3
iti= 3
time = 0
time_of_each_trial = list()
for i in result_trials:
    if i in [labels_outcomes['rewardedBoth'], labels_outcomes['poke1only'], labels_outcomes['poke2only'] ]:
        time+=iti
    time+=waitTime
    time_of_each_trial.append(time)

# plot outcomes vs time
fig, ax = plt.subplots()
first = 0
last = 50
line, = ax.plot (time_of_each_trial[first:last], result_trials[first:last])
plt.yticks([1,2,3,4])
print(len(result_trials))
def animate(i):
    global first, last
    first,last= first+1, last+1
    if last == len(time_of_each_trial):
        print("repeat")
        last = 50
        first = 0
    line.set_xdata(time_of_each_trial[first:last])
    line.set_ydata(result_trials[first:last])
    ax.set_xlim(time_of_each_trial[first], time_of_each_trial[last])
    return line,


ani = animation.FuncAnimation( fig, animate, interval=80, frames=(len(result_trials)-50), repeat=True, )
writervideo = animation.FFMpegWriter(fps=10) 
ani.save("./stage1_lastday.mp4", writer=writervideo)
#plt.show()