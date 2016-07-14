# class BugTester(object):

#     def init(self):
#         self.d={

def makeDict(l, d = {}):
    l.append(d.copy())

l = []

makeDict(l)
makeDict(l)

l[0]['a']= 1
