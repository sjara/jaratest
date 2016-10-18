#!/bin/bash


#Shell script to download ephys data from jaraphys3 for current mice. current mice are'd1pi015','d1pi016'

#jaraphys3 ip address is 184.171.85.90; jaraphys2 ip address is 184.171.85.85

for MOUSE in 'd1pi014' 
do
    rsync -a --progress jarauser@184.171.85.90:data/ephys/$MOUSE /home/languo/data/ephys/
done


