import copy

adap021 = {
    #Muscimol 0.125mg/ml
    'muscimol0125' : ['20160803a', '20160808a', '20160810a', '20160812a'],
    #Saline for muscimol 0.125mg/ml
    'saline_muscimol0125' : ['20160802a', '20160804a', '20160809a', '20160811a'],
    #Muscimol 0.25 mg/ml (WIP)
    'muscimol0250' : ['20160816a', '20160818a'],
    #Saline for muscimol 0.250mg/ml
    'saline_muscimol0250' : ['20160815a', '20160817a', '20160819a']
}


adap028 = {
    #Saline for 0.125mg/ml
    'saline_muscimol0125' : ['20160728a', '20160726a', '20160723a'],
    #Muscimol 0.125 mg/ml
    'muscimol0125' : ['20160729a', '20160727a', '20160725a', '20160721a'],
    #Muscimol 0.0625 mg/ml
    'muscimol00625' : ['20160722a'],
    #Saline for muscimol 0.25mg/ml
    'saline' : ['20160720a', '20160718a', '20160715a', '20160713a'],
    #Muscimol 0.250mg/ml
    'muscimol0250' : ['20160719a', '20160716a', '20160714a', '20160712a'],
}
#Adap028 and adap029 were run together
adap029 = copy.deepcopy(adap028)

adap022 = {'muscimol': ['20160601a', '20160603a', '20160607a', '20160609a', '20160611a'],
           'saline': ['20160531a', '20160602a', '20160606a', '20160608a', '20160610a']}

adap026 = {'muscimol': ['20160601a', '20160603a', '20160607a', '20160609a', '20160611a'],
           'saline': ['20160531a', '20160602a', '20160606a', '20160608a', '20160610a']}

adap027 = {'muscimol': ['20160601a', '20160603a', '20160607a', '20160609a', '20160611a'],
           'saline': ['20160531a', '20160602a', '20160606a', '20160608a', '20160610a']}

adap030 = {'muscimol': ['20160601a', '20160603a', '20160607a', '20160609a', '20160611a'],
           'saline': ['20160531a', '20160602a', '20160606a', '20160608a', '20160610a']}

adap023 = {'muscimol': ['20160429a', '20160501a', '20160503a', '20160505a', '20160507a', '20160509a'],
           'saline': ['20160428a', '20160430a', '20160502a', '20160504b', '20160506a', '20160508a']}

animals = {'adap028':adap028,
           'adap029':adap029,
           'adap022':adap022,
           'adap026':adap026,
           'adap027':adap027,
           'adap030':adap030,
           'adap023':adap023}
