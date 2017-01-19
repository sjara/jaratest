import sys
from jaratest.nick.notification import emailer
import datetime
from taskontrol.settings import rigsettings
from local import secrets
import traceback as tb
import socket

def emailer_excepthook(ertype, erval, traceback):
    '''
    Can be used as a sys.excepthook

    The idea is to log the error, then check to see when the last email was sent
    and not send another email if the time between is too short. This prevents
    cascading failures from sending tons of emails all at once.
    '''

    tb.print_exception(ertype, erval, traceback)
    logfile = rigsettings.DEFAULT_LOG_FILE
    subject, body = format_exception(ertype, erval, traceback)
    now = datetime.datetime.now()
    if os.path.exists(logfile):
        lastTime = last_log_time(logfile)
        if now > lastTime + datetime.timedelta(minutes=30):
            send_email(subject, body)
            log_exception(body)
        else: #Not enough time has passed
            log_exception(body)
    else: #The logfile did not exist
        send_email(subject, body)
        log_exception(body)

def log_exception(formatted_exception, logfile):
    now = datetime.datetime.now()
    nowString = now.strftime('%Y-%m-%d %H:%M:%S')
    f = open(logfile, 'a')
    f.write('ERROR\n')
    f.write(nowString)
    f.write('\n')
    f.write(formatted_exception)
    f.write('\n')
    f.close()

def last_log_time(logfile):
    f = open(logfile, 'r')
    logtext = f.read()
    splits = logtext.split("ERROR")
    lastSplit = splits[-1]
    timestring = lastSplit.split("\n")[1]
    time = datetime.datetime.strptime(timestring, '%Y-%m-%d %H:%M:%S')
    return time

def format_exception(ertype, erval, traceback):
    hostname = socket.gethostname()
    subject = 'ERROR at {}'.format(hostname)
    body = '\n'.join(tb.format_exception(ertype, erval, traceback))
    return subject, body

def send_email(subject, body):
    mailer = emailer.Emailer(secrets.EMAIL, secrets.PASS)
    message = emailer.construct_message(subject, body)
    mailer.send_email(secrets.EMAIL, message)
    mailer.tear_down()

def notify_exception(body):
    '''
    Func to send an email, not used as a sys.excepthook
    '''
    mailer = emailer.Emailer(secrets.EMAIL, secrets.PASS)
    hostname = socket.gethostname()
    subject = 'ERROR at {}'.format(hostname)
    message = emailer.construct_message(subject, body)
    mailer.send_email(secrets.EMAIL, message)
    mailer.tear_down()


# if __name__=="__main__":
    # sys.excepthook = my_excepthook
    # print 'Before Exception'
    # raise RuntimeError('This is the error message')
    # print 'After Exception'
