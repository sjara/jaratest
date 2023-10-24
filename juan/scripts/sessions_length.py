import common_init
import matplotlib.pyplot as plt
from utils import load_behavior_data as lbd
from utils import plots_for_analysis as pfa

"""
This code is to reproduce the same graphs presented in the question
"Length of sessions (for training or for evaluation): 1h vs 45min vs other?" on the Q&A section.
"""


## DATA COLLECTION FIRST SPAN DATES
data = lbd.collect_behavior_data(
    mice_data={"coop026x027": [("2023-08-15", "2023-08-18")]}
)
## RUN
data_filtered_grouped = lbd.filter_and_group(bins=4, data=data, sessionLen=60)

pfa.barplot_accu_rewards_time(
    data_filtered_grouped, len(data.index.get_level_values(0).unique().tolist())
)

# space between plots
plt.tight_layout()

## DATA COLLECTION SECOND SPAN DATES
data_2 = lbd.collect_behavior_data(
    mice_data={"coop026x027": [("2023-08-11", "2023-08-14")]}
)
## RUN
data_filtered_grouped_2 = lbd.filter_and_group(bins=4, data=data_2, sessionLen=60)

pfa.barplot_accu_rewards_time(
    data_filtered_grouped_2, len(data_2.index.get_level_values(0).unique().tolist())
)

# space between plots
plt.tight_layout()

## SHOW PLOT
plt.show()
