Scripts by Evan Vickers.

* `2p_colocalization`: scripts to estimate percentage of green cells that are also yellow.
* `response_tuning`: scripts to estimate tuning of cells recorded with 2p.

* For 2p colocalization of green (GCaMP8m+) and red (AAVrg-tdTomato) neurons, run the script called "twophoton_green_red_colocalization_cli.py". this gives an output to /home/jarauser/tmp called "mouseID_date_session_plane#_spatial_maps.png". Here is the docstring:
  
""
sound_tuning_redcell_spatial_maps_cli.py

Spatial-map-only CLI for two-photon sound tuning with red-cell classification.

Outputs exactly one PNG whose filename ends with "spatial_maps.png".
The left panel shows preferred AM rate or preferred frequency.
The right panel shows dF/F skewness.

Default output directory is /home/jarauser/tmp, but this can be overridden
with --output-dir.
Examples
--------
AM tuning:
python twophoton_green_red_colocalization_cli.py \
  --subject imag029 --date 20260424 --session 006 --plane 0 \
  --paradigm am_tuning --sound-type AM \
  --suite2p-dir /data/twophoton/imag029_processed/20260424/006/suite2p/plane0

Frequency tuning:
python twophoton_green_red_colocalization_cli.py \
  --subject imag025 --date 20260417 --session 000 --plane 0 \
  --paradigm tuning_curve --sound-type frequency \
  --suite2p-dir /data/twophoton/imag025_processed/20260417/000/suite2p/plane0 \
  --output-dir /data/twophoton/imag025_processed/20260417/000/analysis_outputs
"""

* For 2p  response tuning, run the script called "twophoton_sound_tuning_cli.py" this gives outputs to /home/jarauser/tmp called "mouseID_date_session_plane#_..."tuning_raster", "low_example_cell#", "high_example_cell#", "cell#trace_overlay", "eventlocked_avg", and "AM_tuning_curves". For this script, you do not need to pass the explicit suite2p output directory as it is inferred from the mouseID, date, and session. Here is the docstring:
  
  """
twophoton_sound_tuning_cli.py

CLI pipeline for two-photon sound tuning analysis.

This script generates sound-tuning outputs only:
  1. Event-locked average QC plot
  2. All-cell tuning curves
  3. Responsive-cell tuning raster
  4. Random low-preferred-stimulus example cell
  5. Random high-preferred-stimulus example cell
  6. Overlayed response traces for an example responsive cell
  7. Optional red-split tuning raster if --suite2p-dir is supplied and red labels are available

It does NOT generate green/red/yellow spatial maps or ROI colocalization overlays.

Default output directory:
  /home/jarauser/tmp

Example calls
-------------

AM tuning:
python twophoton_sound_tuning_cli.py \
  --subject imag029 --date 20260424 --session 006 --plane 0 \
  --paradigm am_tuning --sound-type AM

Frequency tuning:
python twophoton_sound_tuning_cli.py \
  --subject imag025 --date 20260417 --session 000 --plane 0 \
  --paradigm tuning_curve --sound-type frequency \
  --output-dir /data/twophoton/imag025_processed/20260417/000/analysis_outputs

AM tuning with optional red-split raster:
python twophoton_sound_tuning_cli.py \
  --subject imag029 --date 20260424 --session 006 --plane 0 \
  --paradigm am_tuning --sound-type AM \
  --suite2p-dir /data/twophoton/imag029_processed/20260424/006/suite2p/plane0
"""

