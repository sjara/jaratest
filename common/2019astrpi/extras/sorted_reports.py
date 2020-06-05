"""
Using the list of quality spikes (manually picked by Matt Nardoci), this
program goes through the folder of reports and seperates the reports into
two new folders of 'Quality_tuning' and 'NonQuality_tuning'. It also saves
an h5 file that contains all the cell information for each cell for later
use incase cluster numbers in the database change.
"""
import os
import re
import pandas as pd
import shutil as sh
from jaratoolbox import celldatabase

SAVE = 1

listOfQualitySpikes = [516, 537, 622, 735, 737, 795, 810, 821, 899, 1363,
                       1391, 1402, 1441, 1442, 1444, 1472, 1476, 1479,
                       1506, 1511, 1539, 1632, 1635, 1637, 1639, 1642,
                       1757, 1782, 1863, 1955, 1982, 1984, 1987, 2007,
                       2012, 2029, 2031, 2034, 2052, 2056, 2060, 2077,
                       2084, 2163, 2181, 2186, 2204, 2285, 2286, 2530,
                       2960, 2999, 3085, 3109, 3112, 3154, 3155, 3162,
                       3164, 3185, 3211, 3217, 3230, 3238, 3243, 3354,
                       3359, 3388, 3390, 3395, 3419, 3434, 3466, 3526,
                       3527, 3632, 3710, 3716, 3723, 3921, 3945, 3999,
                       4036, 4038, 4427, 4494, 4507
                       ]

clusterSearch = re.compile("c#[\d]{3,4}")

dataframePath = "/var/tmp/figuresdata/2019astrpi/sorted_cell_index.h5"
folderPath = "/var/tmp/figuresdata/2019astrpi/reports_freq_tuned_cells_in_db"
sortedFolder = "/var/tmp/figuresdata/2019astrpi/Quality_tuning"
badSSFolder = "/var/tmp/figuresdata/2019astrpi/NonQuality_tuning"
counter = 0
# dictOfQuality = {'subject': [],
#                  'date': [],
#                  'depth': []}
dfOfTunedCells = pd.DataFrame()

for dirPath, dirName, fileList in os.walk(folderPath):
    for indFile, file in enumerate(fileList):
        phrase, = clusterSearch.findall(file)
        file_info = re.split('\ |_|\.', file)
        if int(phrase[2:]) in listOfQualitySpikes:
            # sh.move(os.path.join(folderPath, file), os.path.join(sortedFolder, file))
            print(os.path.join(folderPath, file))
            file_info = re.split('\ |_|\.', file)
            clusterNumberInDB = int(file_info[0].strip("[]")[2:])
            date = file_info[1]
            subject = file_info[2]
            depth = float(file_info[3])
            tetrode = int(file_info[5][-1])
            cluster = int(file_info[6][-1])
            quality = 'yes'
            dfOfTunedCells.at[indFile, 'subject'] = subject
            dfOfTunedCells.at[indFile, 'date'] = date
            dfOfTunedCells.at[indFile, 'depth'] = depth
            dfOfTunedCells.at[indFile, 'tetrode'] = tetrode
            dfOfTunedCells.at[indFile, 'cluster'] = cluster
            dfOfTunedCells.at[indFile, 'quality'] = quality
            dfOfTunedCells.at[indFile, 'dbClusterNumber'] = clusterNumberInDB
            counter += 1
        else:
            # sh.move(os.path.join(folderPath, file), os.path.join(badSSFolder, file))
            file_info = re.split('\ |_|\.', file)
            clusterNumberInDB = int(file_info[0].strip("[]")[2:])
            date = file_info[1]
            subject = file_info[2]
            depth = float(file_info[3])
            tetrode = int(file_info[5][-1])
            cluster = int(file_info[6][-1])
            quality = 'no'
            dfOfTunedCells.at[indFile, 'subject'] = subject
            dfOfTunedCells.at[indFile, 'date'] = date
            dfOfTunedCells.at[indFile, 'depth'] = depth
            dfOfTunedCells.at[indFile, 'tetrode'] = tetrode
            dfOfTunedCells.at[indFile, 'cluster'] = cluster
            dfOfTunedCells.at[indFile, 'quality'] = quality
            dfOfTunedCells.at[indFile, 'dbClusterNumber'] = clusterNumberInDB
            print("Hello")
print(counter, len(listOfQualitySpikes))
if SAVE:
    celldatabase.save_hdf(dfOfTunedCells, dataframePath)
"""
title = '[{5}]{0}, {1}, {2}um, T{3}c{4}, session ={6}'.format(
        dbRow['subject'], dbRow['date'], dbRow['depth'], tetnum, chanum,
        dbRow.name, sessions)        
"""