# JWST Little Red Dot Line-Broadening Test Pipeline

This folder provides a minimal, reproducible scaffold for running the proposed JWST test of scattering-dominated line broadening in Little Red Dots (LRDs).
It focuses on public MAST data (NIRSpec + NIRCam) and mirrors the test definition from the prompt: Doppler-only vs Doppler+electron-scattering line fits.

## Scope

The pipeline is intentionally split into discrete scripts so each step can be inspected and rerun:

1. **Fetch public data** from MAST for a candidate LRD list (optionally include Stage-0 rate products).
2. **Reprocess rate products** with the official JWST calibration pipeline (Stage 1/2, optional Stage 3).
3. **Select targets** with broad Balmer lines and compact morphologies.
4. **Fit line profiles** using Doppler-only vs Doppler+scattering models and compare evidence.

## Folder layout

```
./
├── data/               # raw & intermediate data downloads
├── notebooks/          # optional exploration notebooks
├── results/            # fit products & plots
└── scripts/            # pipeline scripts
```

## Quick start

1. Create a virtual environment and install requirements:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Fetch data from MAST for a list of candidate LRDs:

```bash
python scripts/01_fetch_mast.py \
  --targets data/lrd_targets.csv \
  --outdir data/mast_downloads \
  --include-rate
```

3. (Optional) Calibrate a Stage-0 rate file through the official JWST pipeline:

```bash
python scripts/00_calibrate_jwst.py \
  --rate-file data/mast_downloads/<target>/jw0xxxxxx_nrs*_rate.fits \
  --output-dir data/pipeline_outputs
```

4. Run the selection step to identify viable spectra:

```bash
python scripts/02_select_lrd.py \
  --spectra-dir data/mast_downloads \
  --outdir data/selected
```

5. Fit Doppler-only vs Doppler+scattering models:

```bash
python scripts/03_fit_lines.py \
  --input-dir data/selected \
  --results-dir results
```

## Input format

`data/lrd_targets.csv` should contain (at minimum) the following columns:

- `target_name`
- `ra_deg`
- `dec_deg`
- `redshift`
- `preferred_line` (Halpha or Hbeta)

## Notes

- The scripts are scaffolding with clear TODO blocks for implementation details.
- The calibration script wraps the STScI `jwst` pipeline for Stage 1/2 (and optional Stage 3) processing.
- The fitting workflow expects line profile modeling with a Doppler component plus an electron-scattering kernel.
- See the `03_fit_lines.py` docstring for the current modeling skeleton.
