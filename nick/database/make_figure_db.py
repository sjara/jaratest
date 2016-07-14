
from jaratoolbox.test.nick.database import cellDB

dbFn = '/home/nick/data/database/nick_thalamus_cells.json'
db = cellDB.CellDB()
db.load_from_json(dbFn)



figuredb = cellDB.CellDB()
figuredb.append(db[0])
figuredb.append(db[8])
figuredb.append(db[10])
figuredb.append(db[1])

figuredb[0].comments='B/C/D Option -  site 1 T6c3 (Thalamus)'

figuredb[1].comments='B/C/D (our favorite so far), also possibly J - site 6 T6c3 (Thalamus)'

figuredb[2].comments='J - site4 T3c10 (Thalamus)'

figuredb[3].comments='K - site1 T6c6 (Thalamus)'


cortexFn = '/home/nick/Desktop/cortexdb.json'
cortexdb = cellDB.CellDB()
cortexdb.load_from_json(cortexFn)

for cell in cortexdb:
    figuredb.append(cell)


amdbFn = '/home/nick/Desktop/amdatabase.json'
amdb = cellDB.CellDB()
amdb.load_from_json(amdbFn)

figuredb.append(amdb[0])

figdbFn = '/home/nick/Desktop/figure_cells/figure_cells.json'
figuredb.write_to_json(figdbFn)
