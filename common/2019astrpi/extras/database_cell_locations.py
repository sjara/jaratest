import os
import imp
import nrrd
import numpy as np
import pandas as pd
from allensdk.core.mouse_connectivity_cache import MouseConnectivityCache

from jaratoolbox import histologyanalysis as ha
from jaratoolbox import settings
import studyparams


def cell_locations(db):
    """
    This function takes as argument a pandas DataFrame and adds new columns.
    The filename should be the full path to where the database will be saved. If a filename is not specified, the database will not be saved.
    
    This function computes the depths and cortical locations of all cells with suppression indices computed.
    This function should be run in a virtual environment because the allensdk has weird dependencies that we don't want tainting our computers.
    """
    
    # lapPath = os.path.join(settings.ATLAS_PATH, 'AllenCCF_25/coronal_laplacian_25.nrrd')
    # lapPath = '/mnt/jarahubdata/tmp/coronal_laplacian_25.nrrd'
    # TODO Edit the lapPath to be something more descriptive of what it actually is. Also should not use laplacian for non-cortical areas
    # lapPath = settings.LAP_PATH
    # lapData = nrrd.read(lapPath)
    # lap = lapData[0]
    
    mcc = MouseConnectivityCache(resolution=25)
    rsp = mcc.get_reference_space()
    rspAnnotationVolumeRotated = np.rot90(rsp.annotation, 1, axes=(2, 0))
    
    tetrodetoshank = {1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4}  # hardcoded dictionary of tetrode to shank mapping for probe geometry used in this study

    try:
        bestCells = db.query('rsquaredFit>{}'.format(studyparams.R2_CUTOFF))  # calculate depths for all the cells that we quantify as tuned
    except pd.core.computation.ops.UndefinedVariableError:
        bestCells = db

    db['recordingSiteName'] = ''  # prefill will empty strings so whole column is strings (no NaNs)
    
    for dbIndex, dbRow in bestCells.iterrows():
        subject = dbRow['subject']
        
        try:
            fileNameInfohist = os.path.join(settings.INFOHIST_PATH, '{}_tracks.py'.format(subject))
            tracks = imp.load_source('tracks_module', fileNameInfohist).tracks
        except IOError:
            print("No such tracks file: {}".format(fileNameInfohist))
        else:
            # TODO Replace this with a more generic way of finding the brain areas for histology saving.
            brainArea = dbRow['brainArea']
            if brainArea == 'left_AudStr':
                brainArea = 'LeftAstr'
            elif brainArea == 'right_AudStr':
                brainArea = 'RightAstr'
            tetrode = dbRow['tetrode']
            shank = tetrodetoshank[tetrode]
            recordingTrack = dbRow['info'][0]  # This line relies on someone putting track info first in the inforec

            track = next((track for track in tracks if (track['brainArea'] == brainArea) and (track['shank'] == shank) and (track['recordingTrack']==recordingTrack)),None)

            if track is not None:
                histImage = track['histImage']
                
                filenameSVG = ha.get_filename_registered_svg(subject, brainArea, histImage, recordingTrack, shank)

                if tetrode%2==0:
                    depth = dbRow['depth']
                else:
                    depth = dbRow['depth'] - 150.0  # odd tetrodes are higher
                
                brainSurfCoords, tipCoords, siteCoords = ha.get_coords_from_svg(filenameSVG, [depth], dbRow['maxDepth'])
                
                siteCoords = siteCoords[0]
                
                atlasZ = track['atlasZ']
                # cortexDepthData = np.rot90(lap[:, :, atlasZ], -1)
                #
                # # We consider the points with depth > 0.95 to be the bottom surface of cortex
                # bottomData = np.where(cortexDepthData > 0.95)
                #
                # # Top of cortex is less than 0.02 but greater than 0
                # topData = np.where((cortexDepthData < 0.02) & (cortexDepthData > 0))
                #
                # # Distance between the cell and each point on the surface of the brain
                # dXTop = topData[1] - siteCoords[0]
                # dYTop = topData[0] - siteCoords[1]
                # distanceTop = np.sqrt(dXTop**2 + dYTop**2)
                #
                # # The index and distance to the closest point on the top surface
                # indMinTop = np.argmin(distanceTop)
                # minDistanceTop = distanceTop.min()
                #
                # # Same for the distance from the cell to the bottom surface of cortex
                # dXBottom = bottomData[1] - siteCoords[0]
                # dYBottom = bottomData[0] - siteCoords[1]
                # distanceBottom = np.sqrt(dXBottom**2 + dYBottom**2)
                # minDistanceBottom = distanceBottom.min()
                #
                # # The metric we want is the relative distance from the top surface
                # cellRatio = minDistanceTop / (minDistanceBottom + minDistanceTop)
                # db.at[dbIndex, 'cortexRatioDepth'] = cellRatio
                
                # use allen annotated atlas to figure out where recording site is
                thisCoordID = rspAnnotationVolumeRotated[int(siteCoords[0]), int(siteCoords[1]), atlasZ]
                structDict = rsp.structure_tree.get_structures_by_id([thisCoordID])
                print("This is {}".format(str(structDict[0]['name'])))
                db.at[dbIndex, 'recordingSiteName'] = structDict[0]['name']

                # Saving the coordinates in the dataframe
                db.at[dbIndex, 'x-coord'] = siteCoords[0]
                db.at[dbIndex, 'y-coord'] = siteCoords[1]
                db.at[dbIndex, 'z-coord'] = atlasZ
                
            else:
                print(subject, brainArea, shank, recordingTrack)
    
    return db
