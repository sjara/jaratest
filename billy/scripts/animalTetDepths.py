'''
Author: Billy Walker
This script keeps track of tetrode lengths relative to the longest tetrode and the range that the tetrodes are in the striatum

oneAnimal = tetrodeDepths.tetLength('ANIMAL_NAME',
                                    tetrodeLengthList=[TT1,TT2,TT3,TT4,TT5,TT6,TT7,TT8], This is the length of each tetrode relative to the longest tetrode as seen in the animal wiki pages (in mm)
                                    depth_range_striatum=[from depth,to depth], this is the range of depth in mm that the tetrodes were in the auditory striatum
                                    ap_coord = XXmm, This is the distance in mm of the tetrodes from the most posterior point of the striatum as determined by the slices
                                    ml_coord = 'inside' if the tetrodes were in the middle of the striatum, 'medial' if they miss the striatum medially, 'lateral' if they missed the striatum laterally)
tetDB.append_animal(oneAnimal)
'''


import tetrodeDepths

tetDB = tetrodeDepths.tetDatabase()

oneAnimal = tetrodeDepths.tetLength(animalName='test089',
                                    tetrodeLengthList=[0.110,0.310,0.460,0.570,0.230,0.430,0.000,0.000],
                                    depth_range_striatum=[2.38,3.14],
                                    ap_coord = 0.7,
                                    ml_coord = 'inside',
                                    brain_side = 'right')
tetDB.append_animal(oneAnimal)#(0.317*1.25)+2mm = 2.38, (0.317*(4.875-1.25)*(5.5/8.5)+(0.317*1.25+2mm))=3.14 

oneAnimal = tetrodeDepths.tetLength(animalName='test059',
                                    tetrodeLengthList=[0.100,0.510,0.610,0.610,0.190,0.930,0.280,0.000],
                                    depth_range_striatum=[2.6,3.43],
                                    ap_coord = 0.4,
                                    ml_coord = 'inside',
                                    brain_side = 'right')
tetDB.append_animal(oneAnimal)#(0.317*2)+2mm=2.6, (0.317*4.5)+2mm = 3.43

oneAnimal = tetrodeDepths.tetLength(animalName='test017',
                                    tetrodeLengthList=[0.504,0.000,0.209,0.209,0.209,0.705,0.459,0.504],
                                    depth_range_striatum=[3.265,3.83],
                                    ap_coord = 0.5,
                                    ml_coord = 'inside',
                                    brain_side = 'right')
tetDB.append_animal(oneAnimal)#(0.317*4)+2mm=3.265, (0.317*(6-4))*(5.3/6)+(0.317*4)+2mm=3.83

oneAnimal = tetrodeDepths.tetLength(animalName='adap020',
                                    tetrodeLengthList=[0.210,0.230,0.000,0.480,0.380,0.610,0.480,0.380],
                                    depth_range_striatum=[2.6,3.71],
                                    ap_coord = 0.3,
                                    ml_coord = 'inside',
                                    brain_side = 'right')
tetDB.append_animal(oneAnimal)#(0.317*5.375)+2mm=3.71, (0.317*2)+2mm=2.6 when the sound response is found

oneAnimal = tetrodeDepths.tetLength(animalName='adap015',
                                    tetrodeLengthList=[1.260,0.260,0.540,0.340,0.000,0.240,0.110,0.320],
                                    depth_range_striatum=[2.0,3.00],
                                    ap_coord = 0.5,
                                    ml_coord = 'inside',# (guessed this bc there is a big hole)
                                    brain_side = 'right')
tetDB.append_animal(oneAnimal)#(0.317*4.25)*(5.5/7.5)+2mm=3.00
#THIS MOUSE HAD A BIG HOLE WHERE THE TETRODES WERE SO THE RANGE MIGHT BE WRONG

oneAnimal = tetrodeDepths.tetLength(animalName='adap013',
                                    tetrodeLengthList=[0.420,0.530,0.000,0.080,0.490,0.140,0.230,0.360],
                                    depth_range_striatum=[2.0,3.11],
                                    ap_coord = 0.6,
                                    ml_coord = 'inside',
                                    brain_side = 'right')
tetDB.append_animal(oneAnimal)#(0.317*3.5)+2mm = 3.11mm

oneAnimal = tetrodeDepths.tetLength(animalName='adap017',
                                    tetrodeLengthList=[0.050,0.000,0.600,0.190,0.140,0.410,0.310,0.430],
                                    depth_range_striatum=[2.0,3.17],
                                    ap_coord = 0.4,
                                    ml_coord = 'inside',
                                    brain_side = 'right')
tetDB.append_animal(oneAnimal)#(0.317mm*5.00)*(6.5/7.5)+2mm=3.17mm

oneAnimal = tetrodeDepths.tetLength(animalName='test055',
                                    tetrodeLengthList=[0.170,0.170,0.000,0.050,0.090,0.170,0.170,0.170],
                                    depth_range_striatum=[2.35,3.27],
                                    ap_coord = 0.7,
                                    ml_coord = 'inside',
                                    brain_side = 'right')
tetDB.append_animal(oneAnimal)#(0.317*4.25)+1mm=2.35mm   (0.317mm*(9.25-4.25))*(5.5/9.5)+2.35mm=3.27mm
#THIS MOUSE WAS IMPLANTED AT 1MM INSTEAD OF 2MM SO THE RANGE MIGHT BE OFF

oneAnimal = tetrodeDepths.tetLength(animalName='test053',
                                    tetrodeLengthList=[0.140,0.000,0.320,0.440,0.260,0.640,0.580,0.190],
                                    depth_range_striatum=[2.0,3.27],
                                    ap_coord = 0.6,
                                    ml_coord = 'inside',
                                    brain_side = 'right')
tetDB.append_animal(oneAnimal)#(0.317mm*4.00)+2mm=3.27mm
