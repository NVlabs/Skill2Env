# HPC Runtime Diagnosis Patterns

Collect these facts before changing simulation parameters:

- scheduler script and submitted command
- stdout and stderr
- module list
- executable path and version
- MPI launcher and MPI library
- OpenMP variables
- GPU device visibility and accelerator backend
- scratch path and cleanup policy
- restart file cadence

Common fixes should be tested one at a time. Changing resources, physics settings, and executable builds together makes failure diagnosis unreliable.
