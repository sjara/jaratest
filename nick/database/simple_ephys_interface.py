from jaratoolbox.test.nick.database import ephysinterface
reload(ephysinterface)

#Some sessions from 2015-06-24 for reference. 
# d1site1 = day1.add_site(depth = 3543, tetrodes = [6])
# d1site1.add_session('15-22-29', None, sessionTypes['nb'])
# d1site1.add_session('15-27-37', None, sessionTypes['lt'])
# d1site1.add_session('15-31-48', 'a', sessionTypes['tc'])
# d1site1.add_session('15-45-22', 'b', sessionTypes['bf'])

interface = ephysinterface.EphysInterface('pinp003', '2015-06-24', 'nick', 'laser_tuning_curve')

#Plotting session rasters seems to work when providing an ind
# interface.plot_session_raster(-1, 6)
# interface.plot_session_raster('19-16-41', 6, replace=1)

#interface.plot_array_raster(-1)

#This is working as expected. 

# interface.plot_sorted_tuning_raster('15-31-48', 6, 'a')


# interface.plot_session_tc_heatmap('15-31-48', 6, 'a')

# interface.plot_array_freq_tuning('15-31-48', 'a')

interface.flip_tetrode_tuning('15-31-48', 'a')

