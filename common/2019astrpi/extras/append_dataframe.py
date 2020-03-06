import pandas as pd
from jaratoolbox import celldatabase


def append_dataframe(df1, df2):
    """
    Takes two dataframes and concatenates them so we can process one mouse at a time
    instead of having to regenerate an entire database when we add on a new mouse
    Args:
        df1 (string): Full path to dataframe
        df2 (string): Full path to second dataframe

    Returns:
        new_df (pandas.DataFrame): Two given dataframes appended through index value

    """
    pass
