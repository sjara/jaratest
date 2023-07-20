import load_behavior_data as lbd

# import plots_for_analysis as pfa
import argparse

if __name__ == "__main__":
    ## Parse arguments
    parser = argparse.ArgumentParser(
        prog="python main.py",
        description="""Make plots for social cooperation project. This tool receives a excel file with two columns: ids and dates. 
        dates column: All dates desired for a given pair of mice are inside squared brackets (key_mice:[dates]), 
        inside the squared brakets range of dates are inside parenthesis, and individual dates without them.
        ids column: only the first number of the pair is stored in this column, so for 'coop014x015' the key is '14'.
                    """,
        epilog="Author: Juan Picon Cossio",
    )

    ## create subcommands for each plot
    subparsers = parser.add_subparsers(title='Subcommads',help="""subcommands to generate plots for social
                                    cooperation project""", required=True)

    ## Plot percentage rewarded trials
    parser_pct = subparsers.add_parser(
        name="pct_rewarded_trials",
        help="""This is a categorical scatter plot for analyze the percentage of regarded trials against barriers
                So, for each pair of mice is going to plot a graph with the percentage of rewarded trials for each barrier.""",
    )
    parser_pct.add_argument(
        "excelName", help="""Excel file containing two columns: ids and dates. Where in ids column is stored the first number of the pair and
        in dates column a list with ranges of dates inside parenthesis and individual dates without them, E.g.[('2023-05-12','2023-6-16', '2023-7-1')]  """
    )
    ## Plot rewarded trials
    parser_rt = subparsers.add_parser(
        name="rewarded_trials",
        help="""This is a categorical scatter plot for analyze the number of trials between different barriers.
                The developer can filter by the outcome of preference.
                0 = total of trials, 1 = both mice pokes, 2 = only track 1 mouse poke, 3 = only track 2 mouse poke and 4 = None.
                So, for each pair of mice is going to plot a graph with the trials for each barrier."""
    )
    parser_rt.add_argument(
        "excelName", help="""Excel file containing two columns: ids and dates. Where in ids column is stored the first number of the pair and
        in dates column a list with ranges of dates inside parenthesis and individual dates without them, E.g.[('2023-05-12','2023-6-16', '2023-7-1')]  """
    )
    
    parser_rt.add_argument(
        "--filt_outcome_by",
        help="Select the outcome desired to plot",
        choices=[0, 1, 2, 3, 4],
        nargs="*",
        type=int
    )

    args = parser.parse_args()
    print(args)
    # df = lbd.get_dates_from_excel(args.excelName)
    # #df = lbd.collect_behavior_data(mice_data=args.data_dict)
    # print(df)
    # if args.pct_rewarded_trials != None:
    #     pfa.pct_rewarded_trials(df)
