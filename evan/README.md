# Two-photon analysis scripts

Scripts by Evan Vickers.

## 2p green-red colocalization

For two-photon colocalization of green `GCaMP8m+` and red `AAVrg-tdTomato` neurons, run:

```bash
python twophoton_green_red_colocalization_cli.py \
  --subject --date --session --plane \
  --paradigm --sound-type \
  --suite2p-dir (optional)
```

This writes an output file to:

```text
/tmp
```

with the filename format:

```text
mouseID_date_session_plane#_spatial_maps.png
```

Example calls
--------
AM tuning:

```bash
python twophoton_green_red_colocalization_cli.py \
  --subject imag029 --date 20260424 --session 006 --plane 0 \
  --paradigm am_tuning --sound-type AM \
  --suite2p-dir /data/twophoton/imag029_processed/20260424/006/suite2p/plane0 \
  --output-dir /data/twophoton/imag029_processed/20260424/006/analysis_outputs
```

Frequency tuning:

```bash
python twophoton_green_red_colocalization_cli.py \
  --subject imag025 --date 20260417 --session 000 --plane 0 \
  --paradigm tuning_curve --sound-type frequency \
  --suite2p-dir /data/twophoton/imag025_processed/20260417/000/suite2p/plane0 \
  --output-dir /data/twophoton/imag025_processed/20260417/000/analysis_outputs
```

## 2p sound response tuning

For two-photon sound response tuning, run:

```bash
python twophoton_sound_tuning_cli.py \
  --subject --date --session --plane 0 \
  --paradigm --sound-type \
  --suite2p-dir (optional)
```

This writes outputs to:

```text
/tmp
```

with filenames beginning with:

```text
mouseID_date_session_plane#_...
```

Expected output types include:

- `tuning_raster`
- `low_example_cell#`
- `high_example_cell#`
- `cell#trace_overlay`
- `eventlocked_avg`
- `AM_tuning_curves`

For this script, you do **not** need to pass the explicit Suite2p output directory. It is inferred from the mouse ID, date, and session.

Example calls
-------------

AM tuning:

```bash
python twophoton_sound_tuning_cli.py \
  --subject imag029 --date 20260424 --session 006 --plane 0 \
  --paradigm am_tuning --sound-type AM \
  --suite2p-dir /data/twophoton/imag029_processed/20260424/006/suite2p/plane0 \
  --output-dir /data/twophoton/imag029_processed/20260424/006/analysis_outputs
```

Frequency tuning:

```bash
python twophoton_sound_tuning_cli.py \
  --subject imag025 --date 20260417 --session 000 --plane 0 \
  --paradigm tuning_curve --sound-type frequency \
  --suite2p-dir /data/twophoton/imag025_processed/20260417/000/suite2p/plane0 \
  --output-dir /data/twophoton/imag025_processed/20260417/000/analysis_outputs
```