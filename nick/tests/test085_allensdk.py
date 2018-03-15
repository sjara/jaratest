# import numpy as np
# from allensdk.core.mouse_connectivity_cache import MouseConnectivityCache

# mcc = MouseConnectivityCache(resolution=25)
# rsp = mcc.get_reference_space()

# # structures come from an rma query like this:
# # http://api.brain-map.org/api/v2/data/query.json?q=model::Structure,rma::criteria,[graph_id$in1]
# # which does the same thing as using structure_graph_download, but without nesting
# # the graph id is 1
# structures = rsp.structure_tree.nodes()
# ontology_ids = [s['id'] for s in structures]

# # the annotation comes from: http://download.alleninstitute.org/informatics-archive/current-release/mouse_ccf/annotation/ccf_2017/annotation_10.nrrd
# annotation_ids = np.unique(rsp.annotation)

# # this should produce a set whose only element is 0 - the value of out-of-brain voxels
# print( set(annotation_ids) - set(ontology_ids) )

# import nrrd
# annotationFn = '/home/nick/data/jarahubdata/atlas/AllenCCF_25/annotation_25.nrrd'
# # annotationFn = '/home/nick/data/jarahubdata/atlas/AllenCCF_25/coronal_annotation_25.nrrd'
# annotationVol, metadata = nrrd.read(annotationFn)

# annotation_ids = np.unique(annotationVol)
# print( set(annotation_ids) - set(ontology_ids) )


import numpy as np

from allensdk.core.mouse_connectivity_cache import MouseConnectivityCache


def main():
    mcc = MouseConnectivityCache(resolution=10)
    rsp = mcc.get_reference_space()

    # structures come from an rma query like this:
    # http://api.brain-map.org/api/v2/data/query.json?q=model::Structure,rma::criteria,[graph_id$in1]
    # which does the same thing as using structure_graph_download, but without nesting
    # the graph id is 1
    structures = rsp.structure_tree.nodes()
    ontology_ids = [s['id'] for s in structures]

    # the annotation comes from: http://download.alleninstitute.org/informatics-archive/current-release/mouse_ccf/annotation/ccf_2017/annotation_10.nrrd
    annotation_ids = np.unique(rsp.annotation)

    # this should produce a set whose only element is 0 - the value of out-of-brain voxels
print( set(annotation_ids) - set(ontology_ids) )
