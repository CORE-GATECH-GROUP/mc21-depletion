# Data format

This document details the structure of the requisite datafile, `data.h5`.
The following data groups are present, each with a similar format:

- `/reference/serpent` : Data for the half-pin, reflected Serpent reference
- `/serpent/ce/5` : Data for the Serpent predictor case with 5-day depletion steps
- `/serpent/ce/10` : Data for the Serpent predictor case with 10-day depletion steps
- `/hybrid/5` : Data for the hybrid depletion scheme using 5-day coarse depletion steps
- `/hybrid/10` : Data for the hybrid depletion scheme using 10-day coarse depletion steps

Each data group has the following datasets

- `days`: `(N, )` of doubles containing the points in calendar time.
   Used as an index or coordinate vector for other datasets like `keff`
   and `flux`
- `keff`: `(N, )` of doubles containing the multiplication factor.
   `keff[i]` corresponds to day `days[i]`
- `keff_unc`: `(N, )` of doubles containing the absolute uncertainty on
   multiplication factor
- `flux`: `(N, M)` of doubles containing the volume-averaged scalar neutron
  flux in each node over time. `flux[i, j]` corresponds to node `j` at time
  point `i`
- `flux_unc`: `(N, M)` of doubles containing the absolute uncertainty on
  `flux`. Not present for hybrid case as the custom framework does not
  store flux uncertainties. As the hybrid data were generated using
  identical particles per generation, active and inactive generations,
  to the non-reference Serpent cases, the uncertainties in the hybrid
  case will be on a similar scale
- `hfFlags`: `(N, )` of boolean denoting if results provided at point
  `days[i]` were generated from a high-fidelity Monte Carlo simulation
  or the SFV reduced-order solver. Only present for `/hybrid/*` cases.
- `cpuTime`: `(N, )` of double denoting the CPU time for each solution
  step. All cases were performed on similar environments with the same
  number of CPUs and threads
  

# Notes

`/hybrid/*/keff` and the associated uncertainties may be `nan` where the 
reduced-order solution was performed. The SFV method does not currently
perform a prediction on the change in multiplication factor and thus
the value is reported as `nan`.
