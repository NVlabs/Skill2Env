# Workflow Engine Selection Notes

Use a one-off Python script for exploration only. Once a result will be compared, published, screened, or resumed, use a workflow engine or at least a structured manifest.

Common choices:

- atomate2: high-throughput materials workflows, especially VASP/QE/CP2K/force-field workflows using jobflow patterns.
- jobflow: lightweight Python DAGs when you want explicit jobs without a full provenance database.
- AiiDA: provenance-first workflows, remote execution, database-backed records, long-lived campaigns.
- pyiron: interactive atomistic workflows, notebooks, job management, and structure/calculator integration.

Minimum workflow metadata:

- input structure and source
- calculation settings
- code version and executable path
- environment/modules/container image
- scheduler resources
- output files and hashes
- parser version
