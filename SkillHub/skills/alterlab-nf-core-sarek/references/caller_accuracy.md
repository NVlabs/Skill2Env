# Choosing `--tools`: caller selection and accuracy

## The default trap

In nf-core/sarek 3.8.1, **when `--tools` is not specified, the pipeline runs
preprocessing and then Strelka only** (https://nf-co.re/sarek/3.8.1/docs/usage/).
It does not silently run GATK HaplotypeCaller or DeepVariant. Always set
`--tools` to match intent.

## Tool/assay matrix (from the 3.8.1 docs)

Which callers apply to which assay and analysis type:

| Tool (`--tools` value) | WGS | WES | Germline | Tumor-only | Somatic |
|---|:---:|:---:|:---:|:---:|:---:|
| `deepvariant` | x | x | x | | |
| `freebayes` | x | x | x | x | x |
| `haplotypecaller` | x | x | x | | |
| `mutect2` | x | x | | x | x |
| `lofreq` | x | x | | x | |
| `mpileup` | x | x | x | x | |
| `strelka` | x | x | | | x |

(`--tools` also accepts annotation tools such as `snpeff`/`vep`; pass several
comma-separated, e.g. `--tools haplotypecaller,vep`.)

## Recommended choices

| Scenario | `--tools` |
|---|---|
| Germline, GATK4 best practice | `haplotypecaller` |
| Germline, maximize F1 (CNN caller) | `deepvariant` |
| Germline cohort, joint genotyping | `haplotypecaller` + `--joint_germline` |
| Somatic, matched tumor/normal | `mutect2` (or `mutect2,strelka`) |
| Somatic, tumor-only | `mutect2` or `freebayes` |

## Benchmark grounding

nf-core/sarek's own benchmarking study compared callers and infrastructures:

> Hanssen, F., Garcia, M. U., Folkersen, L., Pedersen, A. S., Lescai, F.,
> Jodoin, S., Miller, E., Seybold, M., Wacker, O., Smith, N., Gabernet, G.,
> & Nahnsen, S. (2024). Scalable and efficient DNA sequencing analysis on
> different compute infrastructures aiding variant discovery.
> *NAR Genomics and Bioinformatics, 6*(2), lqae031.
> https://doi.org/10.1093/nargab/lqae031

Reported directional findings (no exact metric values reproduced here — consult
the paper for figures):

- **Germline:** Strelka2 (with Manta) and DeepVariant performed best across the
  evaluated precision/recall/F1 metrics.
- **Somatic:** Mutect2 (filtered) had the highest precision; FreeBayes the
  highest recall; the highest somatic F1 was Mutect2, followed by Strelka2.
- **Aligners:** BWA-MEM and BWA-MEM2 yielded higher recall than DragMap.

Treat these as guidance for `--tools`/`--aligner`, not as a substitute for
benchmarking on your own truth set (e.g. GIAB) when accuracy is critical.
