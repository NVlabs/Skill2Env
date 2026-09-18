# Borzoi — Usage Reference

Deeper detail for `alterlab-borzoi`. Verify the API, weights, and pin against the upstream
`calico/borzoi` README (`TODO(verify)`).

## Install

Install Borzoi per the `calico/borzoi` instructions (TensorFlow/PyTorch variants exist across
forks — confirm which your environment uses) and download the model weights. A CUDA GPU is
recommended because the model ingests a long DNA context.

## Lineage

Borzoi extends the **Enformer** sequence-to-function paradigm to longer context and RNA-seq
coverage prediction. If you have existing Enformer tooling, the concepts (input window,
multi-track output, variant SAD/SED scoring) carry over.

## Predicting tracks

1. Extract the reference sequence window around the locus of interest (coordinates + a genome
   reference, or a FASTA).
2. Run the model to obtain predicted coverage across its output tracks (assays/tissues).

Confirm the exact sequence length, one-hot encoding, and predict call for your version.

## Variant effect scoring

1. Build **reference** and **alternate** sequences for the variant (center the variant in the
   window).
2. Predict tracks for both.
3. Quantify the difference (e.g. SAD/SED-style summaries) to score the regulatory effect.

Prioritize candidate non-coding variants by the magnitude of predicted change. This is a
*prediction* — corroborate with measured data and look up known annotations
(`alterlab-gnomad` for frequency, `alterlab-clinvar` for clinical significance).

## In-silico mutagenesis

Mutate each base across a regulatory element and read predicted-track deltas to localize the
functionally important positions (motif/driver discovery).

## GPU dispatch

Genome-wide or many-variant scans are heavy — dispatch via `alterlab-remote-compute`
(submit → poll → harvest).
