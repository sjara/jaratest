from jaratoolbox import celldatabase
from jaratoolbox import settings
import pandas as pd
import figparams

dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase.h5'
db = pd.read_hdf(dbPath, key='dataframe')

# pinp020 2017-05-09: AnteriorDiI, facingPosterior: All tetrodes actually look good #DONE
#         2017-05-10: DiD, facingPosterior: Only TT1-6 are probably ok #DONE

# pinp025 2017-09-01: AnteriorDiI, facingPosterior: None #DONE
#         2017-09-04: AnteriorDiD, facingPosterior: TT1-2 #DONE

# pinp029 2017-11-08: AnteriorDiI, facingPosterior: TT1-2 #DONE
#         2017-11-09: DiD, facingPosterior: TT5-8 #DONE
#         2017-11-10: PosteriorDiI, facingPosterior: TT7-8 #DONE

