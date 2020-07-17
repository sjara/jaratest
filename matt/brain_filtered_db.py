from jaratoolbox import celldatabase
import studyparams
db = celldatabase.load_hdf("/var/tmp/figuresdata/2019astrpi/direct_and_indirect_cells.h5")
db.columns = [i.replace('-', '_') for i in db.columns]
zDB = db.query("{0} <= 301".format('z_coord'))
zDB2 = db[db['z_coord'].isnull()]
zDBt = pd.concat([zDB, zDB2], axis=0, ignore_index=True, sort=False)
brainDB = zDBt.query("recordingSiteName == 'Caudoputamen' or recordingSiteName == ''")
