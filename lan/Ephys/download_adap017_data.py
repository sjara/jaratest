from subprocess import call 

#call(["mkdir", "/home/languo/data/behavior/billy/adap017/"])
#call(["mkdir", "/home/languo/data/ephys/adap017/"])

call("rsync -a --progress jarauser@jarahub:/data/behavior/billy/adap017/ /home/languo/data/behavior/billy/adap017/".split())

call("rsync -a --progress --exclude '*.continuous' jarauser@184.171.85.85:~/data/ephys/adap017/2016-04-13* /home/languo/data/ephys/adap017/".split())

call("rsync -a --progress --exclude '*.continuous' jarauser@184.171.85.85:~/data/ephys/adap017/2016-04-15* /home/languo/data/ephys/adap017/".split())

call("rsync -a --progress --exclude '*.continuous' jarauser@184.171.85.85:~/data/ephys/adap017/2016-04-19* /home/languo/data/ephys/adap017/".split())

call("rsync -a --progress --exclude '*.continuous' jarauser@184.171.85.85:~/data/ephys/adap017/2016-04-21* /home/languo/data/ephys/adap017/".split())

call("rsync -a --progress --exclude '*.continuous' jarauser@184.171.85.85:~/data/ephys/adap017/2016-04-24* /home/languo/data/ephys/adap017/".split())

call("rsync -a --progress --exclude '*.continuous' jarauser@184.171.85.85:~/data/ephys/adap017/2016-04-26* /home/languo/data/ephys/adap017/".split())

call("rsync -a --progress --exclude '*.continuous' jarauser@184.171.85.85:~/data/ephys/adap017/2016-04-28* /home/languo/data/ephys/adap017/".split())

call("rsync -a --progress --exclude '*.continuous' jarauser@184.171.85.85:~/data/ephys/adap017/2016-05-02* /home/languo/data/ephys/adap017/".split())

call("rsync -a --progress --exclude '*.continuous' jarauser@184.171.85.85:~/data/ephys/adap017/2016-05-04* /home/languo/data/ephys/adap017/".split())

call("rsync -a --progress --exclude '*.continuous' jarauser@184.171.85.85:~/data/ephys/adap017/2016-05-05* /home/languo/data/ephys/adap017/".split())

call("rsync -a --progress --exclude '*.continuous' jarauser@184.171.85.85:~/data/ephys/adap017/2016-05-09* /home/languo/data/ephys/adap017/".split())




call("rsync -a --progress jarauser@jarahub:/data/behavior/billy/adap013/ /home/languo/data/behavior/billy/adap013/".split())

call("rsync -a --progress --exclude '*.continuous' jarauser@184.171.85.85:~/data/ephys/adap013/2016-04-14* /home/languo/data/ephys/adap013/".split())

#call("rsync -a --progress --exclude '*.continuous' jarauser@184.171.85.85:~/data/ephys/adap013/2016-04-05* /home/languo/data/ephys/adap013/".split())

#call("rsync -a --progress --exclude '*.continuous' jarauser@184.171.85.85:~/data/ephys/adap013/2016-04-09* /home/languo/data/ephys/adap013/".split())

#call("rsync -a --progress --exclude '*.continuous' jarauser@184.171.85.85:~/data/ephys/adap013/2016-03-30* /home/languo/data/ephys/adap013/".split())

#call("rsync -a --progress --exclude '*.continuous' jarauser@184.171.85.85:~/data/ephys/adap013/2016-03-28* /home/languo/data/ephys/adap013/".split())

#call("rsync -a --progress --exclude '*.continuous' jarauser@184.171.85.85:~/data/ephys/adap013/2016-03-23* /home/languo/data/ephys/adap013/".split())



'''
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
'''

