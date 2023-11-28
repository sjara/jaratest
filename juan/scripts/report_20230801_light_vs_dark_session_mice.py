import common_init
import utils.load_behavior_data as lbd
import utils.plots_for_analysis as pfa
import matplotlib.pyplot as plt

data = lbd.collect_behavior_data(
    mice_data={
        ## dark vs light (transparent holes)
        # "coop014x015": [("2023-07-17", "2023-07-21"), ("2023-07-23", "2023-07-27")],
        # "coop016x017":[("2023-07-10", "2023-07-14"),("2023-07-16", "2023-07-21"),("2023-07-23", "2023-07-27")],
        # 'coop022x023':[('2023-07-17','2023-07-28')],
        ## dark vs dark (perforated_10_mm and transparent_no_holes)
        # "coop026x027": [("2023-09-11", "2023-09-20")],
        # "coop024x025": [("2023-09-09", "2023-09-17")],
        # "coop022x023": [("2023-09-25", "2023-10-06")],
        ## dark vs light ( transparent no holes)
        # "coop026x027": [("2023-09-27", "2023-09-28"), ("2023-09-30", "2023-10-01"), ("2023-10-03", "2023-10-03")],
        # "coop024x025": [("2023-10-22", "2023-10-27")],
        
        
    }
)
data = lbd.correct_data_with_excel(
    fileName="coop_seek_and_find_v2_updated.xlsx",
    sheet_name=data["MiceID"].unique().tolist(),
    data_collected=data,
)

pfa.pct_rewarded_trials(
    data,
    colors={"perforated_10_mm / dark": "blue", "transparent_no_holes / dark": "purple", "transparent_no_holes / light": "blue"},
    custom_labels={
        "perforated_10_mm / dark": "perf_10_mm\ndark",
        "transparent_no_holes / dark": "transp_no_holes\ndark",
        "transparent_no_holes / light": "transp_no_holes\nlight"
    },
)
plt.show()
