"""
Example for how to save pandas dataframe as beautified HTML.
"""

import pandas as pd
from jaratoolbox import extraplots

dframe = pd.util.testing.makeMixedDataFrame() # Create random dataframe

# Save the dataframe in reverse order
extraplots.dataframe_to_html(dframe.iloc[::-1], '/tmp/myfile.html') 
