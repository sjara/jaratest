from xml.dom import minidom

tree = minidom.parse('/tmp/stritaumTarget.svg')
svg = tree.getElementsByTagName('svg')
docRoot = tree.documentElement



svg0 = svg[0] #The first svg object

groups = svg0.getElementsByTagName('g')

group0 = groups[0]

paths = svg0.getElementsByTagName('path') #Can work regardless of the group

for pathInd, path in enumerate( paths ):
    style = path.getAttribute('style')
    if style:
        styleDict = dict(item.split(':') for item in style.split(';'))

        if styleDict.has_key('stroke-dasharray'):
            if styleDict['stroke-dasharray'] is not 'none':

                

                # print 'yes'



from xml.etree import ElementTree as ET

doc = ET.parse('/tmp/stritaumTarget.svg').getroot()
namespaces = {'svg': 'http://www.w3.org/2000/svg'}

for bigGroup in doc.findall('svg:g', namespaces):
    for miniGroups in bigGroup.findall('svg:g', namespaces):
        for path in miniGroups.findall('svg:path', namespaces):




#This looks like the most promising option


def style_string_to_dict(styleString):
    styleDict = dict(item.split(':') for item in style.split(';'))
    return styleDict

def style_dict_to_string(styleDict):
    styleString = ';'.join(':'.join([key, item]) for key, item in styleDict.iteritems())
    return styleString

import lxml.etree as et

doc = et.parse('/tmp/stritaumTarget.svg')

for element in doc.iter():
    if element.attrib.has_key('style'):
        style = element.attrib['style']
        styleDict = style_string_to_dict(style)
        styleDict['stroke']='#babdb6'
        element.attrib['style'] = style_dict_to_string(styleDict)

f = open('/tmp/newStriatum.svg', 'w')
f.write(et.tostring(doc, pretty_print=True))
f.close()


#This works really well

