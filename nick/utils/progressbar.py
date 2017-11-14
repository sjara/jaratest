import numpy as np
import time
import sys

def progress_bar(done, total, message):
    sys.stdout.flush()
    sys.stdout.write('\r')
    progress = (done/np.double(total))
    sys.stdout.write("%s: [%-20s] %d%%" % (message, '='*np.int(progress*20), np.int(progress*100)))
    sys.stdout.flush()

if __name__=="__main__":
    for ind, item in enumerate(range(200)):
        time.sleep(0.01)
        progress_bar(ind, 200, 'Testing:')
