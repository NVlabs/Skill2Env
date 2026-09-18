# Simulation Failure Patterns

Common first-response mapping:

- NaN/Inf: timestep, invalid material state, division by zero, bad initial geometry.
- Exploding energy or pressure: overlaps, density, force-field mismatch, barostat/thermostat coupling.
- Nonconvergence: residual scaling, preconditioner, initial guess, bad Jacobian, overly tight tolerance.
- Missing potential/pseudopotential: species mapping, file path, functional mismatch, valence mismatch.
- Memory exhaustion (out of memory, bad_alloc, oom-kill): reduce ranks-per-node or domain/grid size, raise per-task memory (--mem/--mem-per-cpu), check per-rank footprint, consider out-of-core options.
- Process crash / memory fault (segfault, SIGSEGV, signal 11, core dumped): out-of-bounds/null-pointer bugs, stack/heap overflow, bad input sizes/indices, insufficient memory/ulimits, library/MPI/BLAS ABI mismatch; reproduce under gdb/valgrind/ASan.
- Corrupted output or incomplete run: walltime, scratch, interrupted writes, disk quota, parallel filesystem.

Retry rules:

1. Preserve evidence.
2. Reduce to the smallest reproducing case.
3. Change one variable at a time.
4. Revalidate physical consistency after numerical recovery.
