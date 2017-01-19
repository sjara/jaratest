import pandas
from jaratest.nick.stats import am_funcs
reload(am_funcs)

# dbfn = '/home/nick/src/jaratest/nick/analysis/poster_ephys/thalamusdb_q10.pickle'
dbfn = '/home/nick/src/jaratest/nick/analysis/poster_ephys/cortexdb_q10.pickle'
database = pandas.read_pickle(dbfn)

for indCell, cell in database.iterrows():
    r_val = am_funcs.am_dependence(cell)
    database.set_value(indCell, 'amRval', r_val)

    highestSync = am_funcs.highest_significant_sync(cell)
    database.set_value(indCell, 'highestSync', highestSync)

database.to_pickle(dbfn)


