#!/bin/bash


#Shell script to download behavior data from jarahub for current mice. current mice are'd1pi015','d1pi016','d1pi014','d1pi017'


for MOUSE in 'd1pi014' 'd1pi018' 'd1pi019' 'd1pi020'
do
    rsync -a --progress jarauser@jarahub:/data/behavior/$MOUSE /home/languo/data/behavior/
done


