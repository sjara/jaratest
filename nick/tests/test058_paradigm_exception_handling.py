import sys
from jaratest.nick.

def my_excepthook(ertype, erval, traceback):
    print "Unhandled error", ertype, erval

sys.excepthook = my_excepthook

print 'Before Exception'

raise RuntimeError('This is the error message')

print 'After Exception'
