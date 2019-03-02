'''
Read ellipse from SVG file and find distance from a point to the ellipse.

Based on old histologyanalysis.get_svg_transform()

NOTE: I didn't finish this because we found a way to use Allen data
      to get cortical depth for each pixel.
'''

filename = '/mnt/jarahubdata/jarashare/histology/anat038/registrationAC/p1d1.svg'
sliceSize=[1040, 1388]

point = np.array([409.1, 81.72]) # Almost touching pia
point = np.array([387.1, 85.7]) # Half-way
point = np.array([381.1, 99.7]) # End of L6

if 1:
    tree = ETree.parse(filename)
    root=tree.getroot()
    images = root.findall('{http://www.w3.org/2000/svg}image')
    if len(images)!=2:
        raise ValueError('The SVG file must contain exactly 2 images')
    if (images[0].attrib['x']!='0') or (images[0].attrib['y']!='0'):
        raise ValueError('The first image (CCF) must be located at (0,0).')
    if images[1].attrib.has_key('transform'):
        transformString = images[1].attrib['transform']
        if transformString.startswith('matrix'):
            transformValueStrings = re.findall(r'-?\d+\.*\d*', transformString)
            transformValues = [float(x) for x in transformValueStrings]
        elif transformString.startswith('rotate'):
            transformValueString = re.findall(r'-?\d+\.*\d*', transformString)[0]
            theta = -np.pi*float(transformValueString)/180 # In radians (and negative)
            # -- Note that this is different from the SVG documentation (b & c swapped) --
            transformValues = [np.cos(theta), -np.sin(theta), np.sin(theta), np.cos(theta)]
    else:
        transformValues = [1,0,0,1,0,0]
    scaleWidth = float(images[1].attrib['width'])/float(sliceSize[0])
    scaleHeight = float(images[1].attrib['height'])/float(sliceSize[1])
    xPos = float(images[1].attrib['x'])
    yPos = float(images[1].attrib['y'])
    scale = np.array([[scaleWidth],[scaleHeight]])
    translate = np.array([[xPos],[yPos]])
    affine = np.reshape(transformValues[:4],(2,2), order='F')

    #return (scale, translate, affine)
