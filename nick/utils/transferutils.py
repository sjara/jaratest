import os
import subprocess
from jaratoolbox import settings

def rsync_session_data(subject,
                       session,
                       server = 'jarauser@jarastore',
                       serverEphysPath = '/data2016/ephys',
                       skipIfExists=False):
    '''
    #TODO: server user and server name as one string
    #TODO: server ephys path and user in settings file
    Rsync just the sessions you need from jarahub
    '''
    fullRemotePath = os.path.join(serverEphysPath, subject, session)
    serverDataPath = '{}:{}'.format(server, fullRemotePath)
    localDataPath = os.path.join(settings.EPHYS_PATH, subject) + os.sep
    fullLocalPath = os.path.join(localDataPath, session)
    transferCommand = ['rsync', '-av', serverDataPath, localDataPath]
    if skipIfExists:
        if not os.path.exists(fullLocalPath):
            subprocess.call(transferCommand)
    else:
        subprocess.call(transferCommand)

def rsync_ISI_file(subject,
                   server = 'jarauser@jarastore',
                   serverEphysPath = '/data2016/ephys',
                   skipIfExists=False):

    isiFn = 'ISI_Violations.txt'
    fullRemotePath = os.path.join(serverEphysPath, '{}_processed'.format(subject), isiFn)
    serverDataPath = '{}:{}'.format(server, fullRemotePath)
    localDataPath = os.path.join(settings.EPHYS_PATH, subject) + os.sep
    transferCommand = ['rsync', '-av', serverDataPath, localDataPath]
    fullLocalFilename = os.path.join(localDataPath, isiFn)
    if skipIfExists:
        if not os.path.isfile(fullLocalFilename):
            subprocess.call(transferCommand)
    else:
        subprocess.call(transferCommand)
