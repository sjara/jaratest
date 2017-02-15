import copy

adap021 = {
    #Muscimol 0.125mg/ml
    'muscimol0125' : ['20160803a', '20160808a', '20160810a', '20160812a'],
    #Saline for muscimol 0.125mg/ml
    'saline_muscimol0125' : ['20160802a', '20160804a', '20160809a', '20160811a'],
    #Muscimol 0.25 mg/ml
    'muscimol0250' : ['20160816a', '20160818a', '20160822a', '20160824a'],
    #Saline for muscimol 0.250mg/ml
    'saline_muscimol0250' : ['20160815a', '20160817a', '20160819a', '20160823a']
}
#alias "muscimol" to the 0.25mg/ml sessions
adap021.update({'muscimol':adap021['muscimol0250']})
#alias "saline" to the sessions collected when we were doing
#0.25mg/ml muscimol sessions
adap021.update({'saline':adap021['saline_muscimol0250']})

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
#alias "muscimol" to the 0.25mg/ml sessions
adap028.update({'muscimol':adap028['muscimol0250']})

#Adap028 and adap029 were run together
adap029 = copy.deepcopy(adap028)

adap023 = {'muscimol': ['20160429a', '20160501a', '20160503a', '20160505a'],
           'saline': ['20160428a', '20160430a', '20160502a', '20160504b']}

adap032 = {'muscimol0250': ['20161130a', '20161202a', '20161204a', '20161206a'],
           'saline': ['20161129a', '20161201a', '20161203a', '20161205a']}
#alias "muscimol" to the 0.25mg/ml sessions
adap032.update({'muscimol':adap032['muscimol0250']})

adap033 = {'muscimol0250': ['20161130a', '20161202a', '20161204a', '20161206a'],
           'saline': ['20161129a', '20161201a', '20161203a', '20161205a'],
           'fluomus': ['20161212a'],
           'fluosal': ['20161209a']}
#alias "muscimol" to the 0.25mg/ml sessions
adap033.update({'muscimol':adap033['muscimol0250']})

adap035 = {'muscimol0250': ['20161130a', '20161202a', '20161204a', '20161206a'],
           'saline': ['20161129a', '20161201a', '20161203a', '20161205a'],
           'fluomus': ['20161208a'],
           'fluosal': ['20161205a']}
#alias "muscimol" to the 0.25mg/ml sessions
adap035.update({'muscimol':adap035['muscimol0250']})

animals = {'adap021':adap021,
           'adap028':adap028,
           'adap029':adap029,
           'adap023':adap023,
           'adap032':adap032,
           'adap033':adap033,
           'adap035':adap035}
