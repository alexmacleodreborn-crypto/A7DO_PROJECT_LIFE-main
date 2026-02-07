"""Fetch JWST NIRSpec/NIRCam data for LRD targets from MAST.

This script uses astroquery.mast to locate public data products and download
calibrated spectra and imaging needed for the LRD line-broadening test.
"""

import argparse
from pathlib import Path

import pandas as pd
from astroquery.mast import Observations


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download JWST LRD data from MAST.")
    parser.add_argument("--targets", required=True, help="CSV of LRD targets.")
    parser.add_argument("--outdir", required=True, help="Output directory for downloads.")
    parser.add_argument(
        "--include-rate",
        action="store_true",
        help="Include Stage-0 rate/rateints products for full pipeline reprocessing.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    targets = pd.read_csv(args.targets)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    for _, row in targets.iterrows():
        target_name = row["target_name"]
        ra_deg = row["ra_deg"]
        dec_deg = row["dec_deg"]
        radius = "3 arcsec"

        obs_table = Observations.query_region(
            f"{ra_deg} {dec_deg}", radius=radius, obs_collection="JWST"
        )
        if len(obs_table) == 0:
            print(f"No JWST observations found for {target_name}.")
            continue

        filtered = obs_table[
            (obs_table["instrument_name"].astype(str).str.contains("NIRSpec"))
            | (obs_table["instrument_name"].astype(str).str.contains("NIRCam"))
        ]
        if len(filtered) == 0:
            print(f"No NIRSpec/NIRCam observations found for {target_name}.")
            continue

        products = Observations.get_product_list(filtered)
        product_groups = ["s2d", "x1d", "cal"]
        if args.include_rate:
            product_groups.extend(["rate", "rateints"])

        calibrated = Observations.filter_products(
            products,
            productSubGroupDescription=product_groups,
            extension=["fits"],
        )

        if len(calibrated) == 0:
            print(f"No calibrated products found for {target_name}.")
            continue

        target_dir = outdir / target_name.replace(" ", "_")
        target_dir.mkdir(parents=True, exist_ok=True)
        Observations.download_products(calibrated, download_dir=str(target_dir))
        print(f"Downloaded {len(calibrated)} products for {target_name}.")


if __name__ == "__main__":
    main()
