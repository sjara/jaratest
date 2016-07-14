from jaratoolbox.test.nick.histology import apply_grid_to_mouse as ag
reload(ag)
bg = ag.BrainGrid('anat030', '2.5', 'left')
bg.define_grid(8)
#bg.convert_grid_coords()
import numpy as np

dg_tip = np.array([795,610])

ctx_thal_lfissure_intersection = np.array([1280,299])

MG_topright = np.array([932,673])

MG_bottomleft = np.array([649,1029])

def transform(coords):
    coordArray = np.array(coords)
    topright = coordArray[coordArray[:,0].argmax(), :] #Greater X
    bottomleft = coordArray[coordArray[:,1].argmax(), :] #Greater Y
    
    transform = np.array([ [348, -374], [146, -419] ]) # Hardcoded, determined empirically

    topright = topright - transform[0, :]
    bottomleft = bottomleft - transform[1, :]
    
    return np.array([topright, bottomleft])
