import sys
from jaratest.nick.notification import emailer
from local import secrets
import traceback as tb
import socket

def emailer_excepthook(ertype, erval, traceback):
    tb.print_exception(ertype, erval, traceback)
    mailer = emailer.Emailer(secrets.EMAIL, secrets.PASS)
    hostname = socket.gethostname()
    subject = 'ERROR at {}'.format(hostname)
    body = '\n'.join(tb.format_exception(ertype, erval, traceback))
    message = emailer.construct_message(subject, body)
    mailer.send_email(secrets.EMAIL, message)
    mailer.tear_down()

def notify_exception(body):
    mailer = emailer.Emailer(secrets.EMAIL, secrets.PASS)
    hostname = socket.gethostname()
    subject = 'ERROR at {}'.format(hostname)
    message = emailer.construct_message(subject, body)
    mailer.send_email(secrets.EMAIL, message)
    mailer.tear_down()


if __name__=="__main__":
    sys.excepthook = my_excepthook
    print 'Before Exception'
    raise RuntimeError('This is the error message')
    print 'After Exception'
