
#rsync -a --progress --exclude '*.continuous' jarauser@jaraphys2:~/data/ephys/test055/ ~/data/ephys/test055/
#rsync -a --progress jarauser@jararig2:/var/tmp/data/santiago/test055/ ~/data/behavior/santiago/test055/
#rsync -a --progress --exclude '*.continuous' jarauser@jaraphys2:~/data/ephys/test017/ ~/data/ephys/test017/
#rsync -a --progress jarauser@jararig2:/var/tmp/data/santiago/test017/ ~/data/behavior/santiago/test017/
#python spikeAnalysis_test017.py
#python spikeAnalysis_test055.py
#python compareRasterAndHistogramClustersOneFreq.py
#python rasterHistPsyCurve.py


#rsync -a --progress ~/data/ephys/test059/reports_clusters/ jarauser@jarahub:/data/reports/cluster_reports/test059/
#rsync -a --progress ~/data/ephys/test086/reports_clusters/ jarauser@jarahub:/data/reports/cluster_reports/test086/
#rsync -a --progress ~/data/ephys/test053/reports_clusters/ jarauser@jarahub:/data/reports/cluster_reports/test053/
#rsync -a --progress ~/data/ephys/test087/reports_clusters/ jarauser@jarahub:/data/reports/cluster_reports/test087/
#rsync -a --progress ~/data/ephys/test089/reports_clusters/ jarauser@jarahub:/data/reports/cluster_reports/test089/
#rsync -a --progress ~/data/ephys/test017/reports_clusters/ jarauser@jarahub:/data/reports/cluster_reports/test017/
#rsync -a --progress ~/data/ephys/test055/reports_clusters/ jarauser@jarahub:/data/reports/cluster_reports/test055/
#rsync -a --progress ~/data/ephys/adap002/reports_clusters/ jarauser@jarahub:/data/reports/cluster_reports/adap002/
#rsync -a --progress ~/data/ephys/adap004/reports_clusters/ jarauser@jarahub:/data/reports/cluster_reports/adap004/
#rsync -a --progress ~/data/ephys/adap010/reports_clusters/ jarauser@jarahub:/data/reports/cluster_reports/adap010/
#rsync -a --progress ~/data/ephys/adap015/reports_clusters/ jarauser@jarahub:/data/reports/cluster_reports/adap015/
#rsync -a --progress ~/data/ephys/adap013/reports_clusters/ jarauser@jarahub:/data/reports/cluster_reports/adap013/
#rsync -a --progress ~/data/ephys/adap017/reports_clusters/ jarauser@jarahub:/data/reports/cluster_reports/adap017/
#rsync -a --progress ~/data/ephys/adap020/reports_clusters/ jarauser@jarahub:/data/reports/cluster_reports/adap020/

#rsync -a --progress --include '*[0-9][0-9].py' --exclude=* ~/src/jaratest/billy/scripts/allcells/ jarauser@jarahub:/data/reports/allcells/ #copies all the allcells_testXXX.py files
#rsync -a --progress --include '*psy.py' --exclude=* ~/src/jaratest/billy/scripts/allcells/ jarauser@jarahub:/data/reports/allcells/ #copies all the allcells_testXXX.py files
#rsync -a --progress --include '*reward.py' --exclude=* ~/src/jaratest/billy/scripts/allcells/ jarauser@jarahub:/data/reports/allcells/ #copies all the allcells_testXXX.py files
rsync -a --progress --include '*_quality.py' --exclude=* jarauser@jarahub:/data/reports/allcells/ ~/src/jaratest/billy/scripts/allcells/ 


#rsync -a --progress ~/data/ephys/test059/reports_clusters/ jarauser@jarahub:/data/reports/cluster_reports/test059/
#rsync -a --progress ~/data/ephys/test086/reports_clusters/ jarauser@jarahub:/data/reports/cluster_reports/test086/
