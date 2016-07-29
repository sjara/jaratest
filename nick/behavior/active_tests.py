#!/usr/bin/env python
import sys; sys.path.append('/home/nick/src')

from jaratest.nick.behavior import behavtests
from jaratest.nick.behavior import emailme
reload(emailme)

subjects = ['amod006', 'amod007','amod008','amod009','amod010']
paradigm = '2afc'
sessionstr = '20160728a'

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

message = []
subject = "Amod behavior report"
for subject in subjects:
    amodtest = behavtests.PercentCorrectAboveAllSoundType(80)
    if amodtest.passes_test(subject, paradigm, sessionstr):
        outcome="[{}{}{}{}]".format(color.BOLD, color.GREEN, "Pass", color.END)
    else:
        outcome="[{}{}{}{}]".format(color.BOLD, color.RED, "Fail", color.END)
    # print outcome
    message.append('{}: {} - {}'.format(outcome, subject, ', '.join(amodtest.message)))

mailer = emailme.EmailMe('email')
text = '\n'.join(message)
email = 'Subject: {}\n\n{}'.format(subject, text)
print email
mailer.send_message(email)




# class TestGroup(object):
#     def __init__(self, subjects, paradigm, sessionstr, test):
#         self.subjects = subjects
#         self.paradigm = paradigm
#         self.sessionstr = sessionstr
#         self.test = test
#         self.message = []
#     def test_all(self):
#         for subject in self.subjects:
#             test = self.test
#             if test.passes_test(subject, self.paradigm, self.sessionstr):
#                 outcome="[{}{}{}{}]".format(color.BOLD, color.GREEN, "Pass", color.END)
#             else:
#                 outcome="[{}{}{}{}]".format(color.BOLD, color.RED, "Fail", color.END)
#             self.message.append('{}: {} - {}'.format(outcome, subject, ', '.join(test.message)))

# test = behavtests.PercentCorrectAboveAllSoundType(80)
# tg = TestGroup(subjects, paradigm, sessionstr, test)

# tg.test_all()
# print '\n'.join(tg.message)

