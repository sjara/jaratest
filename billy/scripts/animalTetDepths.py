import tetrodeDepths

tetDB = tetrodeDepths.tetDatabase()

oneAnimal = tetrodeDepths.tetLength( 'test089',[0.111,0.310,0.460,0.570,0.230,0.430,0.0,0.0],[2.1,3.11])
tetDB.append_animal(oneAnimal)

oneAnimal = tetrodeDepths.tetLength( 'test059',[0.100,0.510,0.610,0.610,0.190,0.930,0.280,0.0],[2.1,3.271])
tetDB.append_animal(oneAnimal)

oneAnimal = tetrodeDepths.tetLength( 'test017',[0.050,0.0,0.600,0.190,0.140,0.410,0.310,0.430],[2.0,3.271])
tetDB.append_animal(oneAnimal)

oneAnimal = tetrodeDepths.tetLength( 'adap020',[0.210,0.230,0.0,0.480,0.380,0.610,0.480,0.380],[2.1,3.8])
tetDB.append_animal(oneAnimal)
