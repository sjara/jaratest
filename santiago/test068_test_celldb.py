'''
Test generating databases for multiple subjects.
'''

from jaratoolbox import celldatabase
reload(celldatabase)

#subjects = ['band062','band072']
subjects = ['pinp019', 'pinp026']

celldb = celldatabase.generate_cell_database_from_subjects(subjects)
#dd = celldatabase.generate_cell_database_from_subjects(subjects,removeBadCells=False)




