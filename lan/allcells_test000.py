'''
List of all isolated units from one animal
'''

from jaratoolbox import celldatabase
reload(celldatabase)
eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()

oneES = eSession(animalName='test000',
                 ephysSession = '2015-02-28_19-02-10',
                 clustersEachTetrode = {1:range(1,13),3:range(1,13)},
                 behavSession = '20150228a')
cellDB.append_session(oneES)

