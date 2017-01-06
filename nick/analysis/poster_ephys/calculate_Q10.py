from jaratest.nick.stats import tuningfuncs
from jaratest.nick.database import dataloader_v2 as dataloader
from matplotlib import pyplot as plt
import numpy as np
import pandas

# dbfn = '/home/nick/src/jaratest/nick/analysis/poster_ephys/thalamusdb_q10.pickle'

dbfn = '/home/nick/src/jaratest/nick/analysis/poster_ephys/cortexdb_q10.pickle'
database = pandas.read_pickle(dbfn)

q10s = []
ixs = []

goodcells = database[(database['noiseburstZ']>2) & (database['isiViolations']<4)]
for index, cell in goodcells.iterrows():

    loader = dataloader.DataLoader(cell['subject'])

    try:
        tuningindex = cell['sessiontype'].index('TuningCurve')
    except ValueError:
        q10s.append(None)
        continue

    bdata = loader.get_session_behavior(cell['behavior'][tuningindex])

    possibleFreq = np.unique(bdata['currentFreq'])
    possibleInten = np.unique(bdata['currentIntensity'])

    #Break out of the loop if the tc does not have enough intensities
    if len(possibleInten)<3:
        q10s.append(np.nan)
        continue

    if len(possibleInten)>6:
        q10s.append(np.nan)
        continue

    zvalArray = tuningfuncs.tuning_curve_response(cell)
    tuner = tuningfuncs.TuningAnalysis(np.flipud(zvalArray), freqLabs = possibleFreq, intenLabs = possibleInten[::-1], thresh=None)

    button = True
    while button:
        button = plt.waitforbuttonpress()
    button = True
    while button:
        button = plt.waitforbuttonpress()
    button = True
    while button:
        button = plt.waitforbuttonpress()
    button = True
    while button:
        button = plt.waitforbuttonpress()
    q10 = tuner.Q10

    database.set_value(index, 'Q10', q10)

# noiseburstSorted = np.array(
#     [250,  75, 142, 132, 248, 249, 255, 186, 140, 127,  78, 208, 134,
#      76, 137,  98, 141, 105,  94,  50,  53,  88, 109,  48, 214, 128,
#      122,  82,  90,  79, 225,  42, 102, 236, 258,  17,  60, 213, 190,
#      21, 202,  68,  13, 150,  31,  11, 139, 168, 170,  12,  16,  15,
#      20,  18, 171, 114, 126,   0,   6,   2, 157, 165, 169,  49,  22,
#      97,  66,  64,  62, 221, 212, 220, 164, 153, 151,  35,  19,  14,
#      83,  61, 182,   5,  52,  65,  58, 123, 215, 237, 205, 161,  44,
#      86,  23, 147, 149, 129, 264,   8, 203, 262, 260, 259, 167, 103,
#      91,  72,  95, 184, 185, 187, 254,  67,  51, 224, 267, 217, 246,
#      219,  46,  27,  32, 113,  85, 112, 183,  57,  54, 226, 211, 263,
#      233,  10, 244, 133,  96,  26,  36,  81, 196,  63, 256, 253,  47,
#      87,  24, 160, 104, 101,  41, 106, 156, 146, 188, 251, 118, 130,
#      239,  89, 229,  25,  99,  73, 172,   1, 163,  37,  29,  92,  80,
#      77, 136, 121, 125, 207,  28,  33,  84, 193, 120,  56, 210, 144,
#      191, 194, 180, 195,  55, 138, 243,  30, 222, 175, 162, 119, 204,
#      238,  74, 131, 245, 148, 135, 228, 115, 252, 117, 124, 223, 216,
#      206, 166, 174, 159, 111,  40,   9,  93, 108, 107,  45, 178, 143,
#      70, 231, 200, 268, 145, 100,   3, 235, 189, 158, 242, 152, 218,
#      116, 173,  59,   4, 261,  71, 176, 192, 179, 110, 227, 198,  39,
#      201, 266, 230, 241,   7,  43, 177,  34, 257, 197, 247, 155, 240,
#      69, 232, 265, 199, 209, 181,  38, 154, 234])

# for index in noiseburstSorted[::-1]:

#     cell=database.ix[index]
#     try:
#         zvalArray = tuning_curve_response(cell)
#         plt.clf()
#         # plt.imshow(np.flipud(zvalArray>2), interpolation='none', cmap='gray')

#         plt.show
#     except ValueError:
#         continue
#     plt.waitforbuttonpress()


#I Think the idea is going to go like this:
## Present a tc to the user
## User clicks on cf
## Draw a line at the right val above threshold
## User clicks on the shoulders of the tc

# Save the values, in frequency (and threshold db) for each cell

# From this, can calculate Q
