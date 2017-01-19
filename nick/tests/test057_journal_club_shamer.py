import mwclient
import re
import smtplib

#This file contains the variables WIKI_LOGIN and WIKI_PASS, among other things
from local import secrets

# MESSAGESUBJECT = 'ATTENTION: Please submit a journal club paper link'
MESSAGESUBJECT = 'TESTING: Please submit a journal club paper link'
# MESSAGEBODY = "You have not yet linked a paper to the JaraLab Journal Club page \
# OR you did not include your initials with the link - use the format (FL) for First, Last"
MESSAGEBODY = "Testing the journal club reminder. Please email me back if this reaches you. \
This email was generated automatically because you have not yet submitted a paper to the \
journal club site."

#TODO Put server etc at top of file as params
def get_wiki_page(page, section):
    site = mwclient.Site(('http','jarahub.uoregon.edu'), path='/mediawiki-1.22.0/')
    site.login(secrets.WIKI_LOGIN,secrets.WIKI_PASS)
    page = site.Pages[page]
    text = page.text(section=section)
    return text


EMAILS = {'SJ': 'sjara@uoregon.edu',
          'LG': 'lan.guo14@gmail.com',
          'NP': 'nponvert@uoregon.edu',
          'AL': 'alakunina@gmail.com',
          'TH': 'theinzer@uoregon.edu',
          'PP': 'phoebepenix@gmail.com'}

# EMAILS = {'SJ': 'sjara@uoregon.edu',
#           'LG': 'lan.guo14@gmail.com',
#           'NP': 'nickponvert@gmail.com'}

def construct_message(subject, message):
    fullMessage = 'Subject: {}\n\n{}'.format(subject, message)
    return fullMessage

class Emailer(object):
    def __init__(self, fromAddr, passwd):
        self.server = smtplib.SMTP()
        self.server.connect('smtp.gmail.com', 587)
        self.server.starttls()
        self.server.login(fromAddr, passwd)
        self.fromAddr = fromAddr
    def send_email(self, message, toAddr):
        self.server.sendmail(self.fromAddr, toAddr, message)
    def tear_down(self):
        self.server.quit()

if __name__=="__main__":

    CASE=0

    if CASE==0: #Test scraping the wiki page
        doneEmails = []
        text = get_wiki_page('JaraLab journal club', 2)
        entries = text.split('* ')
        for entry in entries:

            #Get the initials for the entry
            #TODO: Param for regex
            initialMatch = re.compile("\((..)\)").search(entry)
            if initialMatch:
                initials = initialMatch.groups()[0]
                #TODO initials not in the dict will cause an error here
                email = EMAILS[initials]
                doneEmails.append(email)
                print email

                #Check to see if the entry included a link
                linkMatch = re.search("\[.*\]", entry)
                if linkMatch:
                    print 'DONE'

        em = Emailer(secrets.EMAIL, secrets.PASS)
        message = em.construct_message(MESSAGESUBJECT, MESSAGEBODY)
        for email in EMAILS.values():
            if email not in doneEmails:
                em.send_email(message, email)

    if CASE==1: #Test the emailer
        em = Emailer(secrets.EMAIL)
        messageBody = 'hello world'
        subject = 'emailme.py test'
        message = construct_message(subject, messageBody)
        em.send_email(message)
        em.tear_down()


