'''
Function to select qualified clusters recorded in one session based on cluster quality. Takes clusterQuality, which is a dictionary with Tetrode ID as key and good clusters as value, should contain score for all cluster for all 8 TTs.
'''
import numpy as np
import sys
from jaratoolbox import celldatabase as cellDB

def add_good_cluster_cellDB(clusterQuality):
    clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)}
    for key,value in clusterQuality.items():
        goodClusters = (np.array(value)==1) | (np.array(value)==6)
        clustersEachTetrode[key] = list(np.array(clustersEachTetrode[key])[goodClusters]) 
        
    return clustersEachTetrode

#def write_allcells_good_clusters(oneCell):
    #oneCell is of type cellDB, this function writes a python file (all_cells file) with only the good quality clusters for each session.
    #oneCell.ephysSession=ephysSession
    
        
if __name__ == "__main__":
    clusterQuality={1:[3,4,2,2,2,2,1,1,2,2,1,4],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,2,2,1,2,1,2,2,2,4,1,1],4:[3,1,2,1,3,1,1,2,2,1,4,2],5:[3,1,1,1,2,3,2,1,1,1,2,4],6:[3,3,2,2,4,2,2,4,4,4,4,1],7:[3,1,1,4,3,4,1,2,1,4,2,1],8:[3,1,1,1,4,1,1,2,1,1,1,1]} #this is a dictionary generated after recording and clustering each session based on Billy's criteria
    
    clustersEachTetrode = add_good_cluster_cellDB(clusterQuality)
    print clustersEachTetrode
