import smtplib

class Emailer(object):
    def __init__(self,
                 fromAddr,
                 password,
                 server='smtp.gmail.com',
                 port=587):
        self.fromAddr = fromAddr
        self.server = smtplib.SMTP()
        self.server.connect(server, port)
        self.server.starttls()
        self.server.login(self.fromAddr, password)
    def send_email(self, toAddr, message):
        self.server.sendmail(self.fromAddr, toAddr, message)
    def tear_down(self):
        self.server.quit()

def construct_message(subject, message):
    fullMessage = 'Subject: {}\n\n{}'.format(subject, message)
    return fullMessage

if __name__=='__main__':
    from local import secrets
    em = Emailer(secrets.EMAIL, secrets.PASS)
    messageBody = 'hello world'
    subject = 'emailme.py test'
    message = construct_message(subject, messageBody)
    em.send_email(secrets.EMAIL, message)
    em.tear_down()
