
#rsync -a --progress --include '*_quality*' --exclude=* jarauser@jarahub:/data/reports/allcells/ ~/scripts/allcells/
rsync -a --progress ~/Pictures/interestingPlots/ jarauser@jarahub:/data/reports/interestingPlots/
