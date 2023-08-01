import load_behavior_data as lbd
import plots_for_analysis as pfa
import pandas as pd
import argparse


## Function to process data and get the dataframes with the collected data
def collect_data_df (args) -> pd.DataFrame :
    mice_data_to_collect:dict = lbd.get_dates_from_excel(args.excelName)
    mice_data_collected = lbd.collect_behavior_data(mice_data=mice_data_to_collect)
    return mice_data_collected
    
## default function for subcommand pct_rewarded_trials
def pct_rewarded_trials_subcommand (args):
    mice_data_collected = collect_data_df(args)
    print(mice_data_collected["Date"].unique())
    pfa.pct_rewarded_trials(mice_data_collected)
    

## default function for subcommand rewarded_trials
def rewarded_trials_subcommand (args):
    mice_data_collected = collect_data_df(args)
    print(mice_data_collected["Date"].unique())
    pfa.rewarded_trials(mice_data_collected)



if __name__ == "__main__":
    ## Parse arguments
    parser = argparse.ArgumentParser(
        prog="python cooperate.py",
        description="""Make plots for social cooperation project. This tool receives a mice ID, E.g. coop012x013 and a range of dates, E. g. 2023-05-05x2023-05-15.
                    """,
        epilog="GitHub: juanjo255",
    )

    parser.add_argument(
        "MiceID", help=""" For cooperation project IDs are made up of the word 'coop' followed by two 3-digits number separated by an 'x', E. g. 'coop000x000'"""
    )
    parser.add_argument(
        "Dates", help=""" Range of dates in the format yyyy-mm-dd separated by an 'x', E. g. 2023-05-05x2023-05-15"""
    )
    parser.set_defaults(collect_data_df)

    ## Parse arguments
    args = parser.parse_args()
    ## Call the default function
    args.func(args)


