This folder contains the source files associated with the project "Neural activity trajectories in response to natural sounds"

- `test161_raster_natural_sounds.py`: This file plots the raster plots for every neuron for all the trials of natural sound presentation organized by instance number and category for the experiment session "test161".
- `natural_sounds_rasters.py`: This file plots the raster plots for every neuron for all the trials of natural sound presentation organized by instance number and category.
- `time_aligned_matrix.py`: This file creates a 2D array of the number of spike counts for each cell for every time bin. Dimensions = (num of cells x time bins). The values inside the matrix represent the number of spikes for the particular neuron at a particular time bin.
- `time_aligned_matrix_with_trajectory.py`: This file builds upon the `time_aligned_matrix.py` file to plot the neural trajectory of 2 cells.
- `time_aligned_matrix_with_all_trajectories.py`: This file builds upon the `time_aligned_matrix_with_trajectory.py` file to plot the trajectories of two different cells for all instances.
- `time_aligned_matrix_all_instances.py`: This file creates a 3D array of the number of spike counts for each cell for every time bin. Dimensions = (instance_id x num of cells x time bins)
- `time_aligned_matrix_all_instances_with_pca.py`: This file then applies the NumPy PCA algorithm to the 3D array obtained from `time_aligned_matrix_all_instances.py`
- `time_aligned_matrix_all_instances_with_distance.py`: This file calculates the distance as a function of time between any two different instances.
- `time_aligned_matrix_all_categories_inter_distance.py`: This file calculates the distance as a function of time between the instances of any two different categories.
- `neuralTrajectory.py`: This is an external module that contains all the custom defined functions for plotting the neural trajectories and the distances between instances and categories.
- `neural_trajectory_pipeline.py`: This script builds the pipeline from creating time_aligned_matrix for all instances, performing PCA, plotting the PCA trajectories, plotting intra-category instance distance, and finally plotting inter-category instance distance.
