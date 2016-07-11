from jaratoolbox import histologyanalysis
reload(histologyanalysis)

bg = histologyanalysis.BrainGrid('anat030','1.25',nRows=3,nCols=3)
bg.define_grid(31)

bg.quantify(bg.image)
filesR = bg.filename_stack('r')
stack = bg.load_stack(filesR)
avgIntensity = bg.quantify_stack(stack)

