"""Select LRD spectra with broad Balmer lines and compact morphology.

This step scans downloaded spectra for candidate broad Halpha/Hbeta lines and
pairs them with compact NIRCam imaging products.
"""

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Select LRD spectra for fitting.")
    parser.add_argument("--spectra-dir", required=True, help="Directory of MAST downloads.")
    parser.add_argument("--outdir", required=True, help="Output directory for selected data.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    spectra_dir = Path(args.spectra_dir)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    # TODO: implement parsing of JWST x1d/s2d products with specutils.
    # TODO: estimate line widths for Halpha/Hbeta using redshift metadata.
    # TODO: record compactness metrics from NIRCam imaging.
    # TODO: copy or symlink candidate files into outdir.

    print(f"Selection scaffold ready. Input: {spectra_dir}, Output: {outdir}")


if __name__ == "__main__":
    main()
