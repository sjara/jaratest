import numpy as np


#Channel numbers for the tetrodes
#Shanks from left to right, looking from the top
#Tetrodes from top to bottom, each shank
#Sites clockwise starting with the uppermost site

A4X2TET=np.array([[4, 7, 5, 2], [3, 8, 6, 1], [12, 15, 13, 10], [11, 16, 14, 9], [20, 23, 21, 18], [19, 24, 22, 17], [28, 31, 29, 26], [27, 32, 30, 25]])

#The electrode a32 connector package. Electrode numbers from left to right, top to bottom (4x10 np.array)
#GND = -1
#REF=-2
#UNASSIGNED=-3
A32_CONNECTOR_PACKAGE = np.array([
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
A32_ADAPTOR = np.array([
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
OM32_ADAPTOR = np.array([
    [-1, 23, 25, 27, 29, 31, 19, 17, 21, 11, 15, 13, 1, 3, 5, 7, 9, -2],
    [-2, 24, 26, 28, 30, 32, 20, 18, 22, 12, 16, 14, 2, 4, 6, 8, 10, -1]
])

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




#The omnetics connector on the headstage (chip facing up)
#Not including the four stabilizing pins
#18x2 matrix, top row left to right, then bottom row left to right
#GND = -1
#REF=-2
OM32_HEADSTAGE = np.array([
    [-1, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, -2],
    [-2, 24, 25, 26, 27, 28, 29, 30, 31, 0, 1, 2, 3, 4, 5, 6, 7, -1]
])







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




def convert_to_hs(tet):
    #The corresponding channels on the a32 adaptor
    tet_adaptor = [a32_adaptor[where(a32_electrode==x)] for x in tet]
    #The corresponding channels on the headstage
    tet_hs = [int(om32_headstage[where(om32_adaptor==x)]) for x in tet_adaptor]
    return tet_hs

#the headstage channels for each tetrode
def convert_electrode(tetrodeNp.Array):
    for indTet, tet in enumerate(tetrodeNp.Array):
        thisTet = convert_to_hs(tet)
        if indTet==0:
            tetConfig=thisTet
        else:
            tetConfig=vstack([tetConfig, thisTet])

    return tetConfig



# output (the headstage channels that correspond to each individual tetrode):
# [30, 27, 20, 21]
# [26, 22, 25, 17]
# [23, 16, 18, 24]
# [28, 31, 29, 19]
# [2, 8, 7, 0]
# [13, 14, 6, 15]
# [4, 11, 10, 1]
# [5, 12, 3, 9]


#Now we want to make a config file for openephys with this information

from xml.dom import minidom


## --- The loop to set each subchannel

channelNp.Array = convert_electrode(tetrodes)

#Parse in the xml file
xmldoc = minidom.parse('/tmp/4TT_02_pinp')

#Find the spike detector node
processors = xmldoc.getElementsByTagName('PROCESSOR')
pnames = [processor.attributes['name'].value for processor in processors]
spikeDetectorIndex = pnames.index(u'Filters/Spike Detector')
sdet = processors[spikeDetectorIndex]

#Get the electrode nodes in the spike detector
electrodes = sdet.getElementsByTagName('ELECTRODE')

#Set the channel value for each channel of the electrode
for indElectrode, electrode in enumerate(electrodes):
    subchannels = electrode.getElementsByTagName('SUBCHANNEL')
    for indChannel, channel in enumerate(subchannels):
        chanVal = channelNp.Array[indElectrode, indChannel]
        channel.attributes['ch']._set_value(str(chanVal))

#Check to make sure the values were set
for indElectrode, electrode in enumerate(electrodes):
    subchannels = electrode.getElementsByTagName('SUBCHANNEL')
    for indChannel, channel in enumerate(subchannels):
        print type(channel.attributes['ch'].value)

#Write the new config file out
xmldoc.writexml( open('/tmp/neuronexus_config', 'w'),
               indent="  ",
               addindent="  ",
               newl='\n')




