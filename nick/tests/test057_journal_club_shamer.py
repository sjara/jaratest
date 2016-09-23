import mwclient
import re
import smtplib

#This file contains the variables WIKI_LOGIN and WIKI_PASS, among other things
from local import secrets

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
          'TH': 'thinzer@uoregon.edu'}

class Emailer(object):
    def __init__(self, toAddr):
        self.server = smtplib.SMTP()
        self.server.connect('smtp.gmail.com', 587)
        self.server.starttls()
        self.server.login(secrets.EMAIL, secrets.PASS)
        self.toAddr = toAddr
    @staticmethod
    def construct_message(subject, message):
        fullMessage = 'Subject: {}\n\n{}'.format(subject, message)
        return fullMessage
    def send_email(self, message):
        self.server.sendmail(secrets.EMAIL, self.toAddr, message)
    def tear_down(self):
        self.server.quit()

if __name__=="__main__":

    CASE=1

    if CASE==0: #Test scraping the wiki page
        text = get_wiki_page('JaraLab journal club', 2)
        entries = text.split('* ')
        for entry in entries:

            #Get the initials for the entry
            initialMatch = re.compile("\((..)\)").search(entry)
            if initialMatch:
                initials = initialMatch.groups()[0]
                email = EMAILS[initials]
                print email

                #Check to see if the entry included a link
                linkMatch = re.search("\[.*\]", entry)
                if linkMatch:
                    print 'DONE'

    if CASE==1: #Test the emailer
        em = Emailer(secrets.EMAIL)
        messageBody = 'hello world'
        subject = 'emailme.py test'
        message = em.construct_message(subject, messageBody)
        em.send_email(message)
        em.tear_down()


