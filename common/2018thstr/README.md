# Workflow for producing databases

## `celldatabase_ALLCELLS_MODIFIED_CLU.h5` (now called `celldatabase_calculated_columns.h5`)
### `generate_cell_database.py`
### `generate_rescued_clusters.py`
   IMPORTANT: All modified CLU files should be removed before re-running this step. 
### `generate_tagged.py`
### `generate_summary_freq_tuning.py`
### `generate_summary_am_sync.py`
### `generate_summary_response_latency.py`
### `generate_summary_monotonicity_index.py`
### `generate_summary_extra_response_stats` with CASE = 1 to calculate onsetivity to CF
### `tests/am_perceptron.py` with CASE = 2 to calculate am rate discrimination
### `tests/am_perceptron.py` with CASE = 5 to calculate am phase discrimination
### `README_resave_databases_20180913.py` to resave databases
### `generate_summary_am_onsetivity.py` for AM onsetivity measures
### `generate_summary_extra_response_stats` with CASE = 3 to calculate max evoked rate to tones



## `celldatabase_NBQX.h5`

TODO: tract database? 

# Figure 1 (Anatomy)
## Panel A
This panel has 2 cartoons and a histology image. 
The histology image is: `anat036_Composite_2.5_25_cropped_660_130_600_800.jpg`
To produce this image, take the `anat036_Composite_2.5.tiff` stack, get slice #25, and crop it.
The crop starts at (660, 130) and is 600x800.
Reduce the brightness for the green (fluorescence) channel until the histogram values are ~600 to ~4700

## Panel B
This panel has an image, and a set of boundaries overlaid. 
### Image
The image is from anat036 p1d3.
* Load anat036 5x thalamus p1d3r.czi and p1d3tl.czi in FIJI
* Merge channels, with p1d3r in the green channel. This is the only way I know to set the color LUT to green, although there may be other ways. 
* Split the channels. You only need the fluorescence channel. 
* Make a rectangular selection, then go to Edit>Selection>Specify.
** Width and Height: 577
** X Coord: 658
** Y Coord: 0
* Image>Crop
* Increase the brightness until the top value of the histogram is ~2500
* Add a scale bar. Follow the instrunctions on the Fiji page in the wiki. 
* Later, overlay a white bar on the Fiji-created scale bar to make the color and thickness correspond with Panel D. 

### Boundaries
The boundaries were created by aligning the TL image to the web version of the Allen Reference Atlas, and then
tracing the boundaries of desired areas. 

## Panel C
Panel C is produced by the figure script (below)

## Panel D
The image is from anat036 p1d2. 
* Load anat036 5x cortex p1d2tl.czi and p1d2r.czi
* Merge channels, with p1d3r in the green channel. This is the only way I know to set the color LUT to green, although there may be other ways. 
* Split the channels. You only need the fluorescence channel. 
* Make a rectangular selection, then go to Edit>Selection>Specify.
** Width and Height: 655
** X Coord: 705
** Y Coord: 270
* Image>Crop
* Increase the brightness until the top value of the histogram is ~2500
* Add a scale bar. Follow the instrunctions on the Fiji page in the wiki. 
* Later, overlay a white bar on the Fiji-created scale bar to make the color and thickness correspond with Panel D. 

### Boundaries
The boundaries were created by aligning the TL image to the web version of the Allen Reference Atlas, and then
tracing the boundaries of desired areas. 

### Inset box
* In Inkscape, after the image was imported
* Duplicate the image. Keep the duplicated copy exactly aligned with the original.
* Make a rectangle shape of the desired inset for panel E.
* Duplicate the rectangle. Lock the two together and rotate them into place over the image (stacked with the duplicate). Use the rectangle to outline the part of the image that will be used as the inset. 
* Unlock the two rectangles. Select the histology image and one of the two rectangles. Clip > Set. 
* The clipped image can now be rotated and scaled as needed for panel E. The remaining rectangle should be left in place over the original image, as it indicates to the reader the portion of the image that is displayed in panel E. 

## Panel E
This panel has an image, generated from Panel D. 
It has a set of labels of depth boundaries of layers. 
TODO: How to generate the layer depths? 
It has a histogram produced by the figure script (below).

## Figure script: `figure_anatomy.py`
**Requires**:

`anat036NonLem.npy`
`anat036ventral.npy`
`anat037NonLem.npy`
`anat037ventral.npy`
`anat043NonLem.npy`
`anat043ventral.npy`
Produced by:
  `generate_summary_anatomy.py`
  **Requires**:
    This requires all the SVG and CSV files produced during registration and cell counting. 
    It also requires the Allen reference atlas, but it will download it if it is not in the directory (uses the Allen API)
  
`anat036_p1d2_cellDepths.npy`
Produced by:
 `generate_summart_cortex_cell_depths.py` 
 **Requires**:
   This requires the coronal average template volume `coronal_average_template_25.nrrd`
   It also requires the laplacian volume `coronal_laplacian_25.nrrd`.
   The laplacian volume needs to be resampled according to the wiki, since it is only available in 10um voxel size. 

# Figure 2 (Method/NBQX)

## Panel A
This panel is a cartoon. 

## Panels B-D
These panels are produced by the figure script (below)

## Figure script: `figure_pinp_method.py`
**Requires**:
`celldatabase_NBQX.h5`
Produced by: 
  `generate_pinp_method.py`
  **Requires**:
    This only requires the inforec for pinp031 and the ephys data. 

# Figure 3 (Noise/laser response)
## Panels A, D
These panels are cartoons

## Panels B, E
These panels are produced by the script `figure_example_noise_laser.py` (below)

## Panels C and F
This requires 2 things. You need the locations of recordings sites, which are generated by the scripts
`figure_recording_tracts_ATh.py` and `figure_recording_tracts_AC.py` (below).
The sites are plotted on top of 3 representative average templage sections. 
We then used the corresponding Allen reference atlas (web version) sections and traced regions. The boundaries of
these regions are saved separately, and need to be overlaid. You use the average template to align the boundaries,
and then delete it so that you are left just with the points and the boundaries. We then added labels. 

## Figure script: `figure_example_noise_laser.py`
**Requires**: 
`celldatabase_ALLCELLS_MODIFIED_CLU.h5`

## Figure script: `figure_recording_tracts_ATh.py`
**Requires**: 
`celldatabase_ALLCELLS.h5`
`coronal_average_template_25.nrrd`

## Figure script: `figure_recording_tracts_AC.py`
**Requires**: 
`celldatabase_ALLCELLS.h5`
`coronal_average_template_25.nrrd`

# Figure 4 (Frequency)

## Figure script: `figure_frequency.py`
**Requires**:
`data_freq_tuning_examples.npz`
Produced by: 
  `generate_example_freq_tuning.py`

`celldatabase_ALLCELLS_MODIFIED_CLU.h5`

# Figure 5 (AM)

## Figure script: `figure_am.py`
**Requires**:
`celldatabase_ALLCELLS_MODIFIED_CLU.h5`

`celldatabase_with_am_discrimination_accuracy.h5`
Produced by: 
  `2018thstr/tests/am_perceptron.py` (with CASE==2). After the script runs, copy the output database to the target location. 

`celldatabase_with_phase_discrimination_accuracy.h5`
Produced by: 
  `2018thstr/tests/am_perceptron.py` (with CASE==5). After the script runs, copy the output database to the target location.
