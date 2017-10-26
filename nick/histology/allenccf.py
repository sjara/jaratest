import json
import pandas
import nrrd
import numpy as np

# structureGraphFn =  '/home/nick/Dropbox/data/allenbrain/ccf/structure_graph.json'
# jsonData = open(structureGraphFn).read()
# data = json.loads(jsonData)
# structureGraph = data['msg']
# structureList = []

class AllenAnnotationVolume(object):
    def __init__(self):
        # self.structureGraphFn =  '/home/nick/Dropbox/data/allenbrain/ccf/structure_graph.json'
        self.structureGraphFn =  os.path.join(settings.ALLEN_ATLAS_DIR, 'structure_graph.json')
        jsonData = open(self.structureGraphFn).read()
        data = json.loads(jsonData)
        self.structureGraph = data['msg']
        structureList = []
        self.structureDF = self.process_structure_graph(self.structureGraph)
        # self.annotationFn = '/home/nick/Dropbox/data/allenbrain/ccf/coronal_annotation_25.nrrd'
        self.annotationFn =  os.path.join(settings.ALLEN_ATLAS_DIR, 'coronal_annotation_25.nrrd')
        annotationData = nrrd.read(self.annotationFn)
        self.annotationVol = annotationData[0]
    def process_structure_graph(self, structureGraph):
        structureList = []
        def process_structure_graph_internal(structureGraph):
            for structure in structureGraph:
                #Pop the children out to deal with them recursively
                children = structure.pop('children', None)
                # Add the structure info to the dataframe
                structureList.append(pandas.Series(structure))
                #Deal with the children
                process_structure_graph_internal(children)
        process_structure_graph_internal(structureGraph)
        df = pandas.DataFrame(structureList)
        return df
    def get_structure(self, coords):
        #coords needs to be a 3-TUPLE (x, y, z)
        structID = int(self.annotationVol[coords])
        name = self.structureDF.query('id == @structID')['name'].values[0]
        return structID, name
    def get_name(self, structID):
            name = self.structureDF.query('id==@structID')['name'].item()
            return structID, name
    def trace_parents(self, structID):
        #TODO: I don't know if the nested function approach will work in an obj
        '''Trace the lineage of a region back to the root of the structure graph'''
        parentTrace = []
        parentNames = []
        def trace_internal(structID):
            parentID = self.structureDF.query('id==@structID')['parent_structure_id']
            if not pandas.isnull(parentID.values[0]):
                parentID = int(parentID)
                parentTrace.append(parentID)
                parentNames.append(self.structureDF.query('id==@parentID')['name'].item())
                trace_internal(parentID)
        trace_internal(structID)
        return parentTrace, parentNames

