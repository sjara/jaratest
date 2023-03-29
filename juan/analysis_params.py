# The first approach will be to compared if a mouse sticks longer to a port if its partner is there too
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import date
from load_behavior_data import collect_events, load_data, collect_behavior_data

#%reset -f
#%cd ../..
# data_1 = load_data("coop010x011", "20230319a")
data_events = collect_events(
    start_subject=(14, 15),
    number_of_mice=1,
    start_date=date(2023, 3, 21),
    end_date=date(2023, 3, 26),
)
data = collect_behavior_data(
    start_subject=(14, 15),
    number_of_mice=1,
    start_date=date(2023, 3, 21),
    end_date=date(2023, 3, 28),
)

# Categorical scatter plot for stage 4 coop014x015
# This to observed if data is enough to start stadistical analysis, not only in quantity, but quality (are they sufficently separated?)
# fig, ax = plt.subplots()
# ax.scatter(x=data["BarrierType"],y=data['Percent rewarded'],c=(data['BarrierType']=="solid").apply(lambda x:int(x)))
# ax.hlines(y=[int(data.loc[data['BarrierType']=='perforated','Percent rewarded'].mean()),
#             int(data.loc[data['BarrierType']=='solid','Percent rewarded'].mean())],xmin=0,xmax=1,colors=['purple','yellow'])

# plt.savefig('coop014x015_stage4.jpg')