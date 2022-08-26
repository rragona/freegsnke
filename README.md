# FreeGSNKE: Free-boundary Grad-Shafranov Newton-Krylov Evolve
This package extends [FreeGS](https://github.com/bendudson/freegs) by adding two new capabilities:
- Temporal evolution using a linearised circuit equation with implicit Euler solver.
- Newton-Krylov method to replace the Picard method in the Grad-Shafranov solver.

Currently, only the MAST-U tokamak configuration is supported.

The present implementation has possibly inaccurate values for coil resistance and plasma resistivity.

## Installation
Building from source is currently the only supported installation method and requires a working conda installation. Currently only Python 3.9 has been tested.

1. Clone this repository and `cd` into the created directory.
2. Set up the conda environment with the command `conda env create -f environment.yml`. This creates a conda environment called `freegsnke` with the dependencies of FreeGSFast and FreeGSNKE.
> **Note**
> If this environment setup step fails, try installing the dependencies with less restrictive version requirements. 
3. Activate this environment with `conda activate freegsnke`.
4. Clone [FreeGSFast](https://github.com/farscape-project/freegsfast) into a directory that is *not* within the FreeGSNKE repository and `cd` into it.
5. Install FreeGSFast by following the instruction in the repository README.
6. `cd` back to the `freegsnke` repository directory and install this package by running `pip install .` from the respository home directory. If you plan on doing development, it is better to install with symlinks: `pip install -e .`.

## Usage
See the Jupyter notebook in the `example/` directory. This requires the notebook package, which is not listed as a requirement of this package.

## Release notes
### 0.3: 26 August 2022
Now using conda for most dependency management. Removed dependency on freegs, replaced with freegsfast.
### 0.2: 26 August 2022
Included a simple model of the wall (resistance values to be tailored). Re-incorporated the Ldot terms in the circuit equation, missing in previous version. These are solved for with a Newton method (over all currents, active and passive). Timestepping necessary for convergence on Ldot is decoupled from the timestepping necessary to integrate the circuit equations (passive structures may require shorter timescales).
