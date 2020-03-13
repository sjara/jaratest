import pandas as pd
from jaratoolbox import celldatabase


def merge_dataframes(df1, df2):
    """
    Takes two dataframes and concatenates them so we can process one mouse at a time
    instead of having to regenerate an entire database when we add on a new mouse
    Args:
        df1 (list): List of strings containing full paths to dataframe(s).
        df2 (string): Full path to second dataframe to which the list of dataframes will be appended to the end of

    Returns:
        new_df (pandas.DataFrame): Two given dataframes appended through index value

    """
    df2 = celldatabase.load_hdf(df2)
    for frame in df1:
        appendedFrame = celldatabase.load_hdf(frame)
        df2 = pd.concat([df2, appendedFrame], axis=0, ignore_index=True, sort=False)

    return df2
