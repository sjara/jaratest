import json
import pandas
import nrrd
import numpy as np

fn = '/home/nick/Dropbox/data/allenbrain/ccf/structure_graph.json'

json_data = open(fn).read()
data = json.loads(json_data)
structureGraph = data['msg']
structureList = []

def process_structure_graph(structureGraph):
    for structure in structureGraph:
        #Pop the children out to deal with them recursively
        children = structure.pop('children', None)
        # Add the structure info to the dataframe
        structureList.append(pandas.Series(structure))
        #Deal with the children
        process_structure_graph(children)

process_structure_graph(structureGraph)
df = pandas.DataFrame(structureList)

annotation = nrrd.read('/home/nick/Dropbox/data/allenbrain/ccf/coronal_annotation_25.nrrd')
annotationVol = annotation[0]
annotationMetadata = annotation[1]

#X, Y, Z
coords = np.array([8625, 1400, 6400])

coordsVoxel = coords/25

#Gives you the id
# structid = int(annotationVol[345, 56, 256])
structid = int(annotationVol[329, 149, 180])
name = df.query('id == @structid')['name']

def trace_parents(df, structID):
    '''Trace the lineage of a region back to the root of the structure graph'''
    parentTrace = []
    parentNames = []
    def trace_internal(df, structID):
        parentID = df.query('id==@structID')['parent_structure_id']
        try:
            parentID = int(parentID)
            parentTrace.append(parentID)
            parentNames.append(df.query('id==@parentID')['name'].item())
            trace_internal(df, parentID)
        except ValueError:
            print parentID
    trace_internal(df, structID)
    return parentTrace, parentNames



