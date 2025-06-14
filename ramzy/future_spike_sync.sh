#! /usr/bin/bash

#################################################################################################################
# This script is for automatically transferring spike-sorted data to jarastore once kilosort is finished. It	#
# 	should run from a WSL terminal either just before or just after starting kilosort. If using futureSort,	#
#	a fourth argument may be provided to indicate how many minutes to wait before checking for kilosort.	#
# 														#
# 	USAGE: '$ sh future_spike_sync.sh subject sessionDate probeDepth'					#
# 		e.g., '$ sh future_spike_sync.sh test000 2025-06-13 3500'					#
#################################################################################################################

subject=$1
sessionDate=$2
probeDepth=$3
EPHYS_DATA_PATH=/mnt/d/neuropixels


if [ "$#" -ne 3 ] && [ "$#" -ne 4 ]; then
	echo "ERRORL: $# arguments provided..."
	echo "This script requires exactly three or four arguments."
	echo "USAGE: '$ sh future_spike_sync.sh subject sessionDate probeDepth'"
	echo "e.g., '$ sh future_spike_sync.sh test000 2025-06-13 3500'"
	exit 1
fi

processedFolder=${EPHYS_DATA_PATH}/${subject}/multisession_${sessionDate}_${probeDepth}um_processed

if [ ! -e $processedFolder ]; then
	echo "ERROR: ${processedFolder}/ does not exist."
	exit 1
fi

if [ "$#" -ge 4 ]; then
	waitTime=$4
else
	waitTime=60
fi

echo "Waiting ${waitTime} minutes..."

sleep $(( waitTime*60 )) # wait one hour (or a user-defined amount of time

while [ ! -e "${processedFolder}/spike_positions.png" ]; do
	echo "Waiting..."
	sleep 600 # wait 10 minutes
done

rsync -av ${processedFolder}/{cluster_Amplitude.tsv,cluster_ContamPct.tsv,cluster_group.tsv,cluster_KSLabel.tsv,spike_clusters.npy} ${processedFolder}_prephy/
rsync -av ${processedFolder}* jarauser@jarastore:/data/neuropixels/${subject}/


