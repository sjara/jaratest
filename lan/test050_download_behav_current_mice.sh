#!/bin/bash


#Shell script to download behavior data from jarahub for current mice. current mice are'd1pi015','d1pi016','d1pi014','d1pi017'


for MOUSE in 'd1pi015' 'd1pi016' 'd1pi014' 'd1pi017'
do
    rsync -a --progress jarauser@jarahub:/data/behavior/$MOUSE /home/languo/data/behavior/
done
