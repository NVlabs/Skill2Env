# MD Analysis Checks

Common prerequisites:

- RDF: positions, periodic cell, species labels, cutoff, bin width.
- Coordination: RDF-informed cutoff or chemistry-informed cutoff.
- MSD/diffusion: unwrapped positions (plus cell and image flags to perform the unwrap), time axis, diffusive time window. Verify the diffusive regime (log-log MSD-vs-time slope ~1) before fitting D = lim MSD/(2*d*t), and apply the Yeh-Hummer 1/L finite-size correction (xi ~= 2.837 for a cubic box) using box length L and shear viscosity eta.
- VACF/VDOS: velocities and uniform time spacing.
- Stress-strain: stress or virial, strain history, deformation direction.
- Bond angles: neighbor definition and species triplets.

Do not fit transport properties across startup transients. Use block averaging or independent trajectories when possible.
