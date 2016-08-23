'''
WORK IN PROGRESS, although it may never be finished. An attempt at making a more object-oriented version of the code to map the tetrode channels to the open ephys GUI
'''

class NNDevice(object):
    '''
    The upper and lower mappings are connected by the ELECTRODE NUMBER, not the physical pin location
    '''
    def __init__(self):
        pass
    def upper_coords_for_flattened_lower(self):
        return [np.where(self.upper==x) for x in self.lower.ravel()]
    def lower_shape(self):
        return np.shape(lower)
    def lower_channel_for_inds(upperInds):
        for indElem, elem in enumerate()


class A4x2tetElectrode(NNDevice):
    def __init__(self):
        self.lower = np.array([[4, 7, 5, 2], #Shank 1 upper
                               [3, 8, 6, 1], #Shank 1 lower... etc.
                               [12, 15, 13, 10],
                               [11, 16, 14, 9],
                               [20, 23, 21, 18],
                               [19, 24, 22, 17],
                               [28, 31, 29, 26],
                               [27, 32, 30, 25]])
        self.upper = np.array([
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


class A32_OM32_Adaptor(NNDevice):
    def __init__(self):
        self.lower = np.array([
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
        self.upper = np.array([
    [-1, 23, 25, 27, 29, 31, 19, 17, 21, 11, 15, 13, 1, 3, 5, 7, 9, -2],
    [-2, 24, 26, 28, 30, 32, 20, 18, 22, 12, 16, 14, 2, 4, 6, 8, 10, -1]
])


c = np.zeros(np.shape(a.lower)).ravel()
for indx, x in enumerate(np.nditer(a.lower)):
    c[indx]=np.where(a.upper==x)
print c.reshape(np.shape(a.lower))

indDict={}
for indRow, row in enumerate(a.lower):
    print row
    for indCol, item in enumerate(row):
        indUpper = np.where(a.upper==item)
        indDict.update({item: indUpper})











class ElectrodeAdaptorChain(object):


chain = [A4X2TET, A32_CONNECTOR_PACKAGE, A32_ADAPTOR, OM32_ADAPTOR, OM32_HEADSTAGE]


class SiliconProbeConfigFile(object):
    def __init__(self, chain):
        '''
        Generate an OpenEphys GUI config file for a specific silicon probe electrode mapping
        Args:
        chain (list of numpy arrays): Each channel map in the signal chain, from the probe
                                      to the headstage. See examples above.
        '''
        self.chain = chain
    def move_up_chain(self):
        '''
        Min configuration: electrode map, connector package, and headstage
        Could also be: electrode map, connector pack, connector adapter, headstage adapter, headstage
        electrode map and connector pack - connected by channel number
        connector pack and connector adapter - connected by pin location
        connector adapter and headstage adapter - connected by channel number
        headstage adapter and headstage - connected by pin location
        Mappings on 2 sides of the same device are connected by channel number
        2 devices, when connected, are connected by pin location
        '''
    def convert_to_next():
        #The corresponding channels on the a32 adaptor
        tet_adaptor = [a32_adaptor[where(a32_electrode==x)] for x in tet]
        #The corresponding channels on the headstage
        tet_hs = [int(om32_headstage[where(om32_adaptor==x)]) for x in tet_adaptor]
        return tet_hs
