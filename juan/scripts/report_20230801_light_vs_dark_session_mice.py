import common_init
import utils.load_behavior_data as lbd
import utils.plots_for_analysis as pfa
import matplotlib.pyplot as plt

data = lbd.collect_behavior_data(
    mice_data={
        "coop014x015": [("2023-07-17", "2023-07-21"), ("2023-07-23", "2023-07-27")],
        "coop016x017":[("2023-07-10", "2023-07-14"),("2023-07-16", "2023-07-21"),("2023-07-23", "2023-07-27")],
        'coop022x023':[('2023-07-17','2023-07-28')]
    }
)
data = lbd.correct_data_with_excel(
    fileName="coop_seek_and_find_v2.xlsx",
    sheet_name=["coop014x015","coop016x017","coop022x023"],
    data_collected=data,
)

pfa.pct_rewarded_trials(data)
pfa.rewarded_trials(data)
plt.show()