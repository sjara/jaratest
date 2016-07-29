import smtplib
from jaratest.nick import localsettings

class EmailMe():
    def __init__(self, mode):
        self.server = smtplib.SMTP("smtp.gmail.com", 587)
        self.server.starttls()
        self.server.login(localsettings.GMAIL_ACCT, localsettings.GMAIL_PASS)
        assert mode in ['email', 'text'], "Mode must be either 'email' or 'text'"
        self.mode = mode

    def send_message(self, messageText):
        if self.mode == 'email':
            toAddr = localsettings.GMAIL_ACCT
        elif self.mode == 'text':
            toAddr = localsettings.TEXT
        self.server.sendmail(localsettings.GMAIL_ACCT, toAddr, messageText)



# #Email myself
# server.sendmail('nickponvert@gmail.com', 'nickponvert@gmail.com', 'Hello World')
# #Text myself
# server.sendmail('nickponvert@gmail.com', '9283003588@vtext.com', 'Hello World')


