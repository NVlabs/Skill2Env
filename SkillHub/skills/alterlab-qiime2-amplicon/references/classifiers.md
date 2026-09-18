# Taxonomic classifiers — version matching is mandatory

`qiime feature-classifier classify-sklearn` (action name verified in the Moving Pictures
tutorial) takes a **pretrained naive-Bayes classifier** `.qza` plus your `rep-seqs.qza`
and emits `taxonomy.qza`.

```bash
qiime feature-classifier classify-sklearn \
  --i-classifier <classifier>.qza \
  --i-reads rep-seqs.qza \
  --o-classification taxonomy.qza
qiime metadata tabulate --m-input-file taxonomy.qza --o-visualization taxonomy.qzv
```

## The #1 trap: classifier must match your QIIME 2 version

A pretrained classifier is a **pickled scikit-learn model**. scikit-learn does not
guarantee unpickling across versions, so a classifier trained for one QIIME 2 release may
**fail to load (or silently misbehave)** under another. Always download the classifier
artifact built for the **exact QIIME 2 release you are running** from the QIIME 2 Library
data resources (the docs note pretrained classifiers are published there as data
resources), or train your own in the same env (below).

## Reference databases by amplicon

| Amplicon | Reference DB | Notes |
|----------|--------------|-------|
| 16S / 18S rRNA | **SILVA 138** | Broad rRNA reference; full-length and region-specific (e.g. 515F/806R) classifiers are published. |
| 16S rRNA | **Greengenes2** (e.g. 2024.09) | Phylogeny-integrated 16S reference; pick the release whose date matches your workflow. |
| Fungal ITS | **UNITE** | The standard ITS reference; use the UNITE-trained classifier, not SILVA. |

Match the **region** too: a classifier trained on the **same primer region** as your reads
(e.g. a 515F/806R V4 extract) generally outperforms a full-length classifier on short
reads. Confirm the exact current classifier filenames/URLs from the QIIME 2 Library before
downloading — do not hardcode a filename that may have moved.

## Train your own (when no pretrained artifact matches)

If no published classifier matches your version + region, train one in the active env:

```bash
# 1. Extract the amplicon region from a reference using YOUR primers
qiime feature-classifier extract-reads \
  --i-sequences ref-seqs.qza \
  --p-f-primer <FORWARD_PRIMER> --p-r-primer <REVERSE_PRIMER> \
  --o-reads ref-seqs-extracted.qza
# 2. Fit the naive-Bayes classifier
qiime feature-classifier fit-classifier-naive-bayes \
  --i-reference-reads ref-seqs-extracted.qza \
  --i-reference-taxonomy ref-taxonomy.qza \
  --o-classifier my-classifier.qza
```

Training is RAM-heavy (full SILVA can need tens of GB) — a good local/offline job. Verify
the exact `extract-reads` / `fit-classifier-naive-bayes` signatures with
`qiime feature-classifier <action> --help` in your env.

## Alternatives to sklearn classification

- `classify-consensus-vsearch` / `classify-consensus-blast` — alignment-based consensus
  classification; no pretrained pickle, so no version-pickle risk (slower, needs the ref
  sequences + taxonomy artifacts). Useful when a matching sklearn classifier is unavailable.

## Sources

- QIIME 2 Moving Pictures tutorial (`feature-classifier classify-sklearn`).
- QIIME 2 amplicon docs (pretrained classifiers published as Library data resources).
- SILVA 138 / Greengenes2 / UNITE are the standard 16S/18S/ITS references; confirm exact
  artifact versions and URLs from the QIIME 2 Library at use time.
