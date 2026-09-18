# Reference Sequence Management (refget)

`gtars.refget` implements the GA4GH refget / sequence-collections protocol:
compute sequence digests, build a local store, and retrieve sequences.
Verified against v0.8.

## Module-level digest functions

```python
from gtars import refget

# Digest an entire FASTA into a GA4GH SequenceCollection
# (computes sequence-level + collection-level digests; does NOT load sequence data)
collection = refget.digest_fasta("hg38.fa")

# Load a FASTA WITH sequence data into a SequenceCollection
collection = refget.load_fasta("hg38.fa")

# One-off digests for a raw sequence
refget.sha512t24u_digest("ACGTACGT")   # GA4GH ga4gh digest: SHA-512 truncated to
                                        # 24 bytes, base64url-encoded -> 32 chars
refget.md5_digest("ACGTACGT")          # legacy MD5 digest

# Single-sequence record (the sequence-level parallel to digest_fasta).
# Signature is digest_sequence(data: bytes, name: str | None = None) -- data
# must be bytes, and is the FIRST argument.
record = refget.digest_sequence(b"ACGTACGT", "chr1")

# FASTA index (.fai) metadata
fai = refget.compute_fai("hg38.fa")
```

## RefgetStore

`RefgetStore` is a queryable store of sequence collections. Create one in memory,
open a local directory, or open a remote store with local caching — there is no
`RefgetStore.from_fasta(...)`; load FASTA via `add_sequence_collection_from_fasta`.

```python
from gtars import refget

# In-memory store (2-bit packed encoding by default)
store = refget.RefgetStore.in_memory()

# Load a reference FASTA into the store
store.add_sequence_collection_from_fasta("hg38.fa")

# Inspect contents
store.list_collections()   # collection metadata + pagination
store.list_sequences()     # per-sequence metadata (no sequence data loaded)

# Open an existing on-disk store, or a remote one with caching
store = refget.RefgetStore.open_local("/path/to/store")
store = refget.RefgetStore.open_remote("https://.../store")
```

### Extracting subsequences

Coordinates are 0-based, half-open `[start, end)`. Sequence data is loaded lazily.
`get_substring` is keyed by the sequence **digest** (sha512t24u), not the name —
look the digest up from `list_sequences()` or use `get_sequence_by_name`.

```python
# list_sequences() returns a list of SequenceMetadata (name, length, sha512t24u, md5, ...)
meta = {s.name: s for s in store.list_sequences()}
chr1_digest = meta["chr1"].sha512t24u

# Extract by digest:
seq = store.get_substring(chr1_digest, 0, 100)

# Collection digest (needed by the region-based helpers below):
coll = store.list_collections()["results"][0].digest

# By name within a collection:
record = store.get_sequence_by_name(coll, "chr1")

# Extract sequences for every region in a BED file (collection_digest first):
seqs = store.substrings_from_regions(coll, "regions.bed")   # list[RetrievedSequence]

# Export to FASTA
store.export_fasta("out.fa")
store.export_fasta_from_regions(coll, "regions.bed", "regions.fa")
```

## Use cases

### Reference validation via digests

```python
from gtars import refget

collection = refget.digest_fasta("reference.fa")
# Compare the collection / per-sequence digests against expected GA4GH digests.
```

### Region extraction

```python
store = refget.RefgetStore.in_memory()
store.add_sequence_collection_from_fasta("hg38.fa")
coll = store.list_collections()["results"][0].digest
seqs = store.substrings_from_regions(coll, "regions_of_interest.bed")
```

### Cross-reference comparison

```python
# Digesting two assemblies and comparing collection-level digests tells you
# whether two references share identical sequence content.
c19 = refget.digest_fasta("hg19.fa")
c38 = refget.digest_fasta("hg38.fa")
```

## Notes

- The GA4GH `ga4gh`/`sha512t24u` digest is SHA-512 truncated to 24 bytes and
  base64url-encoded (32 characters). `md5_digest` is the legacy refget digest.
- `digest_fasta` computes digests without loading sequence bytes; `load_fasta`
  and the `RefgetStore` loaders bring sequence data into memory/cache.
