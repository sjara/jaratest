
'''
2015-07-28 Nick Ponvert
This file is a test of a function or object that will allow the user to analyze many
injections. The workflow will be to first manually define a corners file for each injection,
and then a new function will load the corners automatically and calculate the fluorescence for
the entire stack.

We can then feed this data into a method that will combine all of the positive injections, and
will subtract any negative injections.

Combination method for non-bool values is still up in the air: mean? max? sum?
If we average, will be consider only the injections where the voxel had some
fluorescence? These decisions will affect the logical meaning of our combination.

Removal method - set to 0/min? subtract?

'''
