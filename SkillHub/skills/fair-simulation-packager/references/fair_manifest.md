# FAIR Simulation Manifest Fields

A minimal simulation bundle should include:

- project name and scientific intent
- simulation engine and version
- command line or workflow engine
- input files with SHA-256 hashes
- output files with SHA-256 hashes
- structure identifier or local structure file
- units for reported quantities
- code commit, container digest, or module list
- parser version for derived quantities
- known limitations and failed checks

For NOMAD, OPTIMADE, or Materials Project integration, keep structure identity, composition, lattice, method, and property units explicit.
