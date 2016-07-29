from subprocess import call 

#subprocess.call(["mkdir", "/home/languo/data/behavior/billy/adap015/"])


call("rsync -a --progress jarauser@jarahub:/data/behavior/billy/adap015/ /home/languo/data/behavior/billy/adap015/".split())

call("rsync -a --progress --exclude '*.continuous' jarauser@184.171.85.85:~/data/ephys/adap015/2016-02-04* /home/languo/data/ephys/adap015/".split())

call("rsync -a --progress --exclude '*.continuous' jarauser@184.171.85.85:~/data/ephys/adap015/2016-02-07* /home/languo/data/ephys/adap015/".split())

call("rsync -a --progress --exclude '*.continuous' jarauser@184.171.85.85:~/data/ephys/adap015/2016-02-11* /home/languo/data/ephys/adap015/".split())

call("rsync -a --progress --exclude '*.continuous' jarauser@184.171.85.85:~/data/ephys/adap015/2016-02-15* /home/languo/data/ephys/adap015/".split())

call("rsync -a --progress --exclude '*.continuous' jarauser@184.171.85.85:~/data/ephys/adap015/2016-02-17* /home/languo/data/ephys/adap015/".split())

call("rsync -a --progress --exclude '*.continuous' jarauser@184.171.85.85:~/data/ephys/adap015/2016-02-19* /home/languo/data/ephys/adap015/".split())

call("rsync -a --progress --exclude '*.continuous' jarauser@184.171.85.85:~/data/ephys/adap015/2016-02-22* /home/languo/data/ephys/adap015/".split())

call("rsync -a --progress --exclude '*.continuous' jarauser@184.171.85.85:~/data/ephys/adap015/2016-02-24* /home/languo/data/ephys/adap015/".split())

call("rsync -a --progress --exclude '*.continuous' jarauser@184.171.85.85:~/data/ephys/adap015/2016-02-25* /home/languo/data/ephys/adap015/".split())

call("rsync -a --progress --exclude '*.continuous' jarauser@184.171.85.85:~/data/ephys/adap015/2016-02-29* /home/languo/data/ephys/adap015/".split())

call("rsync -a --progress --exclude '*.continuous' jarauser@184.171.85.85:~/data/ephys/adap015/2016-03-01* /home/languo/data/ephys/adap015/".split())


call("rsync -a --progress --exclude '*.continuous' jarauser@184.171.85.85:~/data/ephys/adap015/2016-03-17* /home/languo/data/ephys/adap015/".split())

call("rsync -a --progress --exclude '*.continuous' jarauser@184.171.85.85:~/data/ephys/adap015/2016-03-18* /home/languo/data/ephys/adap015/".split())
