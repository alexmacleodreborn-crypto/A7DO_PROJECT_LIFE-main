"""Fit LRD emission lines with Doppler-only vs Doppler+scattering models.

The model uses a Doppler-broadened core plus an electron-scattering kernel.
Scattering width is tied to electron temperature:

sigma_scatt = sqrt(k * Te / (m_e * c^2)) * c

This script is a scaffold: it defines the data flow and placeholders for the
actual line-model fitting (e.g., using emcee or dynesty).
"""

import argparse
from pathlib import Path

import numpy as np

K_BOLTZMANN = 1.380649e-23
M_ELECTRON = 9.10938356e-31
C_LIGHT = 299_792_458.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fit line profiles for LRDs.")
    parser.add_argument("--input-dir", required=True, help="Directory of selected spectra.")
    parser.add_argument("--results-dir", required=True, help="Output directory for fits.")
    return parser.parse_args()


def sigma_scattering(te_kelvin: float) -> float:
    return np.sqrt(K_BOLTZMANN * te_kelvin / (M_ELECTRON * C_LIGHT**2)) * C_LIGHT


def main() -> None:
    args = parse_args()
    input_dir = Path(args.input_dir)
    results_dir = Path(args.results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)

    # TODO: read spectra into wavelength/flux arrays.
    # TODO: fit Doppler-only model (e.g., Gaussian/Voigt core).
    # TODO: fit Doppler+scattering model using convolution kernel.
    # TODO: compare Bayesian evidence and save posterior summaries.

    example_te = 2.0e4
    print(f"Example scattering sigma at Te={example_te:.1f} K: {sigma_scattering(example_te):.2f} m/s")
    print(f"Fitting scaffold ready. Input: {input_dir}, Output: {results_dir}")


if __name__ == "__main__":
    main()
