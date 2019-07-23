#!/bin/bash

FILE_SIZE=`stat -c "%s" $1`
FILE_NAME="${1%.*}"
OUTPUT_NAME="${FILE_NAME}_rigid.sbx"

#Make the new sbx file, same size as the original
fallocate -l $FILE_SIZE $OUTPUT_NAME

#Copy over the mat file with the same name
cp ${FILE_NAME}.mat ${FILE_NAME}_rigid.mat
