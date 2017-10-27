from jaratoolbox import celldatabase
import numpy as np

### --- Test inforec file --- ###

subject = 'pinp024'
experiments = []
exp0 = celldatabase.Experiment(subject,
                               '2017-08-15',
                               brainarea='rightAstr',
                               info=['anteriorDiI', 'facingPosterior'])
experiments.append(exp0)
#
exp0.add_site(1853, tetrodes=range(1, 9))
exp0.add_session('14-20-39', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('14-24-06', 'a', 'tc', 'am_tuning_curve')
exp0.add_session('14-42-31', 'b', 'am', 'am_tuning_curve')
#
exp0.add_site(1956, tetrodes=range(1, 9))
exp0.add_session('15-03-00', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('15-06-22', 'c', 'tc', 'am_tuning_curve')
exp0.add_session('15-24-08', 'd', 'am', 'am_tuning_curve')
#
exp0.add_site(2458, tetrodes=range(1, 9))
exp0.add_session('18-41-08', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('18-43-32', 'm', 'tc', 'am_tuning_curve')
exp0.add_session('19-10-44', 'n', 'am', 'am_tuning_curve')

### --- Load the allen CCF and select the start and end of the penetration for SHANK 1 --- ###

shank1Start = np.array([324, 22, 180])
shank1End = np.array([324, 140, 180])
shank1Diff = shank1End - shank1Start
#Compute the vector magnitude (the total length of the penetration in voxels)
shank1Length = np.linalg.norm(shank1Diff)

#Calculate the proportion of max depth for each site
maxDepth = 2458.0
siteDepths = np.array([1853, 1956, 2458])
siteProportions = siteDepths/maxDepth

#Calculate the proportional difference from start (in voxels) for each site
siteProportionalDiff = [shank1Diff * x for x in siteProportions]

#Calculate the coords for each site by adding the proportional diff to the start point
siteCoords = [shank1Start + diff for diff in siteProportionalDiff]

#One of the shanks is used as the zero shank when doing recordings with the probes facing posterior or anterior
zeroShank = 1

#ShankCoords (shankNum, start/end, xyz)
shankCoords = np.array([[[312, 17, 191], [309, 148, 191]],
                        [[326, 20, 191], [321, 149, 191]],
                        [[339, 25, 191], [333, 151, 191]],
                        [[350, 30, 191], [345, 152, 191]]])

#IF we used one of the shanks to do the zero, and if some of the shanks LOOK shorter because of the curvature of the brain, we need to 'extend' the start of the shank so that the length agrees with the zero shank.
def compute_shank_length(start, end):
    shankDiff = end - start
    shankLength = np.linalg.norm(shankDiff)
    return shankLength

def get_new_start_coords_for_non_ref_shanks(shankCoords, refShankInd, refShankLength):
    '''
    Returns new shankCoords with updated start coords for non-ref shanks.
    '''

    # To get the lengths of each probe
    shankDiff = np.diff(shankCoords, axis=1)
    shankLengths = np.linalg.norm(shankDiff, axis=2)
    shankMinusRefShank = shankLengths[refShankInd] - shankLengths
    shankMinusRefShank/shankLengths

    
