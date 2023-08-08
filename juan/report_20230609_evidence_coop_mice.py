import load_behavior_data as lbd
import plots_for_analysis as pfa
import matplotlib.pyplot as plt

data = lbd.collect_behavior_data(
    mice_data={
        "coop012x013":[("2023-05-04", "2023-05-15")],
        "coop014x015": [("2023-05-11", "2023-05-17"), ("2023-06-04", "2023-06-16")],
        "coop016x017":[("2023-05-12", "2023-05-17"),("2023-06-04", "2023-06-16")],
        "coop018x019":[("2023-05-08", "2023-05-19")]
        # 'coop016x017':[('2023-07-10','2023-07-14'),('2023-07-16','2023-07-21'),('2023-07-23','2023-07-27')],
        #'coop022x023':[('2023-07-29','2023-08-03')]
    }
)
data = lbd.correct_data_with_excel(
    fileName="coop_seek_and_find_v2.xlsx",
    sheet_name=['coop012x013',"coop014x015","coop016x017","coop018x019"],
    data_collected=data,
)

pfa.pct_rewarded_trials(data)
pfa.rewarded_trials(data)
plt.show()
