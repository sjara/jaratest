import common_init
import matplotlib.pyplot as plt

import utils.load_behavior_data as lbd
import utils.plots_for_analysis as pfa

data = lbd.collect_behavior_data(
    mice_data={
        "coop012x013": [("2023-05-04", "2023-05-15")],
        "coop014x015": [("2023-05-11", "2023-05-17"), ("2023-06-04", "2023-06-16")],
        "coop016x017": [
            ("2023-05-12", "2023-05-17"),
            ("2023-06-04", "2023-06-16"),
            ("2023-08-23", "2023-09-01"),
        ],
        "coop018x019": [("2023-05-08", "2023-05-19")],
        "coop022x023": [("2023-07-29", "2023-08-03")],
        "coop024x025": [
            ("2023-08-28", "2023-09-07"),
            ("2023-10-04", "2023-10-11"),
            ("2023-10-16", "2023-10-19"),
        ],
        "coop026x027": [("2023-09-01", "2023-09-07"), ("2023-10-04", "2023-10-19")],
    }
)
data = lbd.correct_data_with_excel(
    fileName="coop_seek_and_find_v2_updated.xlsx",
    sheet_name=data["MiceID"].unique().tolist(),
    data_collected=data,
)

pfa.pct_rewarded_trials(data)
pfa.rewarded_trials(data)
plt.show()
