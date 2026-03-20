"""Run the official JWST calibration pipeline on Stage-0 rate data.

This script performs:
  - Stage 1 (Detector1Pipeline) -> rateints
  - Stage 2 (Spec2Pipeline) -> cal
  - Optional Stage 3 (Spec3Pipeline) -> x1d
"""

import argparse
from pathlib import Path

from jwst.pipeline import Detector1Pipeline, Spec2Pipeline, Spec3Pipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calibrate JWST NIRSpec rate products into science-ready spectra."
    )
    parser.add_argument(
        "--rate-file",
        required=True,
        help="Input Stage-0 *_rate.fits file from MAST.",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory to write pipeline products.",
    )
    parser.add_argument(
        "--run-stage3",
        action="store_true",
        help="Run Spec3Pipeline to generate x1d products.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    rate_file = Path(args.rate_file)
    if not rate_file.exists():
        raise FileNotFoundError(f"Rate file not found: {rate_file}")

    stage1 = Detector1Pipeline()
    stage1.output_dir = str(output_dir)
    stage1.save_results = True
    stage1_result = stage1.run(str(rate_file))

    stage2 = Spec2Pipeline()
    stage2.output_dir = str(output_dir)
    stage2.save_results = True
    stage2_result = stage2.run(stage1_result)

    if args.run_stage3:
        stage3 = Spec3Pipeline()
        stage3.output_dir = str(output_dir)
        stage3.save_results = True
        stage3.run(stage2_result)

    print(f"Pipeline complete. Outputs written to {output_dir}")


if __name__ == "__main__":
    main()
