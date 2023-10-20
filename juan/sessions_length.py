import load_behavior_data as lbd
import plots_for_analysis as pfa
import matplotlib.pyplot as plt


"""
This code is to reproduce the same graphs presented in the question
"Length of sessions (for training or for evaluation): 1h vs 45min vs other?" on the Q&A section.
"""


## DATA COLLECTION
data = lbd.collect_behavior_data(
    mice_data={"coop026x027": [("2023-08-15", "2023-08-18")]}
)
## RUN
data_filtered_grouped = lbd.filter_and_group(bins=3, data=data, sessionLen=60)
print(data)
pfa.barplot_accu_rewards_time(data_filtered_grouped, len(data['Date'].unique().tolist()))

## SHOW PLOT
# plt.tight_layout()
# plt.show()