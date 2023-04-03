# The first approach will be to compared if a mouse sticks longer to a port if its partner is there too
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import date
from load_behavior_data import collect_behavior_data

#pd.options.display.float_format = "{:.6f}".format

data_behavior = collect_behavior_data(
    start_subject=(14, 15),
    number_of_mice=1,
    start_date=date(2023, 3, 21),
    end_date=date(2023, 3, 26),
)

# FIRST PART
# How much time elapsed between the first and second poke?

success = data_behavior[data_behavior["Outcome"] == 1].copy()
success.reset_index(inplace=True, drop=True)
success["timeBetweenPokes"] = abs(success["TimePoke1"] - success["TimePoke2"])
indexes = list()
for i in range(1, len(success.index)):
    if success.loc[i, "ActiveSide"] != success.loc[i - 1, "ActiveSide"]:
        indexes.append(i)

alternate = success.loc[indexes]
alternate.groupby(by=['MiceID','BarrierType'])['timeBetweenPokes'].describe()