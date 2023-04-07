from load_behavior_data import collect_data
from datetime import date
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Objective: Explore if using the information of timepoke1 and timepoke2 we can see something about the project
# or we can for example deduce the wait time
data_coop010x011 = collect_data(
    (10,11),
    1,
    start_date=date(2023,3,5),
    end_date=date(2023,3,11)
)
data_coop010x011.drop("Time", axis=1, inplace=True)
data_coop010x011.dropna(subset=['TimePoke1', 'TimePoke2'],inplace=True)
data_coop010x011['timeBetweenPokes'] = abs(data_coop010x011['TimePoke1'] - data_coop010x011['TimePoke2'])

data_coop012x013 = collect_data(
    (12,13),
    1,
    start_date=date(2023,3,4),
    end_date=date(2023,3,10)
)
data_coop012x013.drop("Time", axis=1, inplace=True)
data_coop012x013.dropna(subset=['TimePoke1', 'TimePoke2'],inplace=True)
data_coop012x013['timeBetweenPokes'] = abs(data_coop012x013['TimePoke1'] - data_coop012x013['TimePoke2'])

data_coop014x015 = collect_data(
    (14,15),
    1,
    start_date=date(2023,3,8),
    end_date=date(2023,3,13)
)
data_coop014x015.drop("Time", axis=1, inplace=True)
data_coop014x015.dropna(subset=['TimePoke1', 'TimePoke2'],inplace=True)
data_coop014x015['timeBetweenPokes'] = abs(data_coop014x015['TimePoke1'] - data_coop014x015['TimePoke2'])

df = pd.concat([data_coop010x011,data_coop012x013,data_coop014x015])

fig,ax = plt.subplots(nrows=1,ncols=2)
sns.violinplot(x=df['MiceID'], y=df['timeBetweenPokes'],ax=ax[0])
ax[0].set_title("time between first and second poke from stage 2 and 3")
df_stage_1 = df[df['Stage']==3]
sns.violinplot(x=df_stage_1['MiceID'], y=df_stage_1['timeBetweenPokes'],ax=ax[1])
ax[1].set_title("time between first and second poke from stage 3")
plt.tight_layout()
plt.show()