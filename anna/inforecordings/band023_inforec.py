from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'band023'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2017-03-20', brainarea='right_thalamus', info='anteriorDiI')
experiments.append(exp0)
