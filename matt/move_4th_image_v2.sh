#!/bin/bash

source_Dir="/Users/Matt/Desktop/Research/Murray/data/jarahub/jarashare/widefieldTestSession/low_freq"
destination_Dir="/destiantion/folder/"

echo "Looking for files in $source_Dir"
echo "Will move files to $destination_Dir"

# Get list of image files; change the pattern if not "low_freq_*"
for file in $(find $source_Dir -type f -name "low_freq_*.tif"); do
  # Remove the prefix and the '.tif' extension; change .tif if needed
  number=$(basename "$file" .tif | sed 's/^low_freq_//')
  # Remove leading zeros and check if the number is a multiple of 4
  if [ $((10#${number} % 4)) -eq 0 ]; then
    # rsync -avP --dry-run "$file" "$destination_Dir"
    echo "Rsyncing $file to $destination_Dir"
  fi
done
