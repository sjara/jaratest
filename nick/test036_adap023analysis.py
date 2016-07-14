from jaratoolbox.test.nick import behavioranalysis_vnick as behavioranalysis

'''
Test data analysis for adap023 - this needs work because all of my muscimol overview reports are currently written for data with different sound types


As part of this work, I need to work on my behavioranalysis fxns


'''



# behavior_summary('adap023', ['20160426a', '20160427a','20160428a','20160429a',   '20160430a', '20160501a', '20160502a', '20160503a', '20160504b','20160505a','20160506a','20160507a','20160508a','20160509a', '20160510a']) #left

## -- Plotting the average saline and muscimol psycurves
#NOTE THE b in 0504 below
salineSessions = ['20160428a', '20160430a', '20160502a', '20160504b', '20160506a', '20160508a']
muscimolSessions = ['20160429a', '20160501a', '20160503a', '20160505a', '20160507a', '20160509a']

salineData = behavioranalysis.load_many_sessions('adap023', salineSessions)
muscimolData = behavioranalysis.load_many_sessions('adap023', muscimolSessions)

behavioranalysis.plot_multiple_psycurves([salineData, muscimolData],['k', 'r'])






