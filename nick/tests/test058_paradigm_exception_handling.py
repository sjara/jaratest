import sys
from jaratest.nick.notification import emailer
from local import secrets
import traceback as tb

def my_excepthook(ertype, erval, traceback):
    mailer = emailer.Emailer(secrets.EMAIL, secrets.PASS)
    subject = 'Unhandled exception'
    body = '\n'.join(tb.format_exception(ertype, erval, traceback))
    message = emailer.construct_message(subject, body)
    mailer.send_email(secrets.EMAIL, message)
    mailer.tear_down()

if __name__=="__main__":
    sys.excepthook = my_excepthook
    print 'Before Exception'
    raise RuntimeError('This is the error message')
    print 'After Exception'
