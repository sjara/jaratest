import numpy as np


#Channel numbers for the tetrodes
#Shanks from left to right, looking from the top
#Tetrodes from top to bottom, each shank
#Sites clockwise starting with the uppermost site

A4X2TET=np.array([[4, 7, 5, 2],
                  [3, 8, 6, 1],
                  [12, 15, 13, 10],
                  [11, 16, 14, 9],
                  [20, 23, 21, 18],
                  [19, 24, 22, 17],
                  [28, 31, 29, 26],
                  [27, 32, 30, 25]])

#Entering this for now as 1 big "tetrode"
A1X32_POLY2 = np.array([[23, 10, 24, 9, 25, 8, 26, 7, 27, 6, 28, 5, 29, 4, 30, 3, 31, 2, 32, 1, 22, 11, 21, 12, 20, 13, 19, 14, 18, 15, 17, 16]])

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

####
###
##
#
#Important: You have to turn the probe over to connect it to the adaptor, so one of them needs to be flipped left-right
A32_CONNECTOR_PACKAGE=np.fliplr(A32_CONNECTOR_PACKAGE)
#
##
###
####

#The omnetics connector on the adaptor (neuronexus label facing up)
#Not including the four stabilizing pins
#18x2 matrix, top row left to right, then bottom row left to right
#GND = -1
#REF=-2
OM32_ADAPTOR = np.array([
    [-1, 23, 25, 27, 29, 31, 19, 17, 21, 11, 15, 13, 1, 3, 5, 7, 9, -2],
    [-2, 24, 26, 28, 30, 32, 20, 18, 22, 12, 16, 14, 2, 4, 6, 8, 10, -1]
])

#The omnetics connector on the headstage (chip facing up)
#Not including the four stabilizing pins
#18x2 matrix, top row left to right, then bottom row left to right
#GND = -1
#REF=-2
OM32_HEADSTAGE = np.array([
    [-1, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, -2],
    [-2, 24, 25, 26, 27, 28, 29, 30, 31, 0, 1, 2, 3, 4, 5, 6, 7, -1]
])

####
###
##
#
#Important: The headstage needs to be connected to the adapter with the chip facing the front of the adapter (the omnetics side should have a 'Neuronexus' stamp on this side). This means that the headstage channels, as they are written now, should be flipped left-right as well
OM32_HEADSTAGE = np.fliplr(OM32_HEADSTAGE)
#
##
###
####

def convert_to_hs(tet):
    #The corresponding channels on the a32 adaptor
    tet_adaptor = [A32_ADAPTOR[np.where(A32_CONNECTOR_PACKAGE==x)] for x in tet]
    #The corresponding channels on the headstage
    tet_hs = [int(OM32_HEADSTAGE[np.where(OM32_ADAPTOR==x)]) for x in tet_adaptor]
    return tet_hs

#the headstage channels for each tetrode
def convert_electrode(tetrodes):
    for indTet, tet in enumerate(tetrodes):
        thisTet = convert_to_hs(tet)
        if indTet==0:
            tetConfig=thisTet
        else:
            tetConfig=np.vstack([tetConfig, thisTet])

    return tetConfig


channelMap = convert_electrode(A4X2TET)

iraChannelMap = convert_electrode(A1X32_POLY2)

#The openephys GUI counts from 1, so we need to add 1
channelMap = channelMap + 1

iraChannelMap = np.array(iraChannelMap) + 1

'''
Code to try and generate the config file - I just did it manually for the second mapping
from xml.dom import minidom

## --- The loop to set each subchannel

#Parse in the xml file
xmldoc = minidom.parse('/tmp/neuronexus_config')

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
        chanVal = channelMap[indElectrode, indChannel]
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

'''
