import numpy as np
#Channel numbers for the tetrodes
#Shanks from left to right, looking from the top
#Tetrodes from top to bottom, each shank
#Sites clockwise starting with the uppermost site
 
tetrodes=np.array([[4, 7, 5, 2], [3, 8, 6, 1], [12, 15, 13, 10], [11, 16, 14, 9], [20, 23, 21, 18], [19, 24, 22, 17], [28, 31, 29, 26], [27, 32, 30, 25]])
 
#The electrode a32 connector package. Electrode numbers from left to right, top to bottom (4x10 np.array)
#GND = -1
#REF=-2
#UNASSIGNED=-3
a32_electrode = np.array([
    [32, -1, -1, 11],
    [30, -3, -2, 9],
    [31, -3, -3, 7],
    [28, -3, -3, 5],
    [29, 26, 1, 3],
    [27, 24, 4, 2],
    [25, 20, 13, 6],
    [22, 19, 14, 8],
    [23, 18, 15, 10],
    [21, 17, 16, 12]
])
 
#The adaptor a32 package now. channel numbers from left to right, top to bottom. 4x10 np.array
#GND = -1
#REF=-2
#UNASSIGNED=-3
a32_adaptor = np.array([
    [1, -1, -1, 32],
    [2, -2, -2, 31],
    [3, -3, -3, 30],
    [4, -3, -3, 29],
    [5, 16, 17, 28],
    [6, 15, 18, 27],
    [7, 14, 19, 26],
    [8, 13, 20, 25],
    [9, 12, 21, 24],
    [10, 11, 22, 23]
])
 
#The omnetics connector on the adaptor (neuronexus label facing up)
#Not including the four stabilizing pins
#18x2 matrix, top row left to right, then bottom row left to right
#GND = -1
#REF=-2
om32_adaptor = np.array([
    [-1, 23, 25, 27, 29, 31, 19, 17, 21, 11, 15, 13, 1, 3, 5, 7, 9, -2],
    [-2, 24, 26, 28, 30, 32, 20, 18, 22, 12, 16, 14, 2, 4, 6, 8, 10, -1]
])
 
 
#The omnetics connector on the headstage (chip facing up)
#Not including the four stabilizing pins
#18x2 matrix, top row left to right, then bottom row left to right
#GND = -1
#REF=-2
om32_headstage = np.array([
    [-1, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, -2],
    [-2, 24, 25, 26, 27, 28, 29, 30, 31, 0, 1, 2, 3, 4, 5, 6, 7, -1]
])
 
 
#The channels for a single trode
tet = tetrodes[1,:]
 
 
def convert_to_hs(tet):
    #The corresponding channels on the a32 adaptor
    tet_adaptor = [a32_adaptor[np.where(a32_electrode==x)] for x in tet]
    #The corresponding channels on the headstage
    tet_hs = [int(om32_headstage[np.where(om32_adaptor==x)]) for x in tet_adaptor]
    return tet_hs
 

#Copied from output of below
OLDMAPPING = np.array([
    [30, 27, 20, 21],
    [26, 22, 25, 17],
    [23, 16, 18, 24],
    [28, 31, 29, 19],
    [2, 8, 7, 0],
    [13, 14, 6, 15],
    [4, 11, 10, 1],
    [5, 12, 3, 9],
])

#the headstage channels for each tetrode
if __name__=='__main__':
    for tet in tetrodes:
        print convert_to_hs(tet)

    # output (the headstage channels that correspond to each individual tetrode):
    # [30, 27, 20, 21]
    # [26, 22, 25, 17]
    # [23, 16, 18, 24]
    # [28, 31, 29, 19]
    # [2, 8, 7, 0]
    # [13, 14, 6, 15]
    # [4, 11, 10, 1]
    # [5, 12, 3, 9]
