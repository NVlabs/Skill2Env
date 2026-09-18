# Genomic Tokenizers

Tokenizers map genomic regions onto a fixed vocabulary of discrete tokens for ML
models — the preprocessing layer that `geniml` builds embeddings on top of.

> The class is **`Tokenizer`** (in `gtars.tokenizers`). There is no `TreeTokenizer`.
> Verified against v0.8.

## Building a tokenizer

```python
from gtars.tokenizers import Tokenizer

# Build the vocabulary from a "universe" BED file
tokenizer = Tokenizer.from_bed("universe.bed")

# Or load a saved/published tokenizer
tokenizer = Tokenizer.from_config("tokenizer.toml")
tokenizer = Tokenizer.from_pretrained("databio/...")   # from a hub identifier
```

## Tokenizing regions

`tokenize` accepts a `RegionSet` or a list of `Region` objects (note `Region`'s
4th positional `rest` arg) and returns token **strings**:

```python
from gtars.models import Region, RegionSet

regions = [Region("chr1", 1500, 1800, None), Region("chr2", 5500, 5600, None)]
tokens = tokenizer.tokenize(regions)        # e.g. ['chr1:1000-2000', 'chr2:5000-6000']

# A RegionSet works directly too:
tokens = tokenizer.tokenize(RegionSet("query.bed"))
```

## Tokens to IDs (for the model)

```python
ids = tokenizer.convert_tokens_to_ids(tokens)   # [0, 2, ...]
back = tokenizer.convert_ids_to_tokens(ids)      # token strings

# encode() maps a single token string to its id(s):
tokenizer.encode("chr1:1000-2000")               # -> [0]
```

## Vocabulary and special tokens

```python
tokenizer.vocab_size                 # int
tokenizer.get_vocab()                # {token: id}
tokenizer.special_tokens_map         # {'unk_token': '<unk>', 'pad_token': '<pad>', ...}
tokenizer.unk_token, tokenizer.unk_token_id
tokenizer.pad_token, tokenizer.pad_token_id
tokenizer.mask_token, tokenizer.cls_token, tokenizer.bos_token, tokenizer.eos_token
```

Out-of-universe regions map to the unknown token.

## Tokenizing fragment files directly

For single-cell fragment files, `tokenize_fragment_file` tokenizes fragments in
one call:

```python
from gtars.tokenizers import tokenize_fragment_file
# Signature varies by version; check help(tokenize_fragment_file).
```

## Integration with geniml

`gtars` produces token IDs; `geniml` (skill `alterlab-geniml`) trains the embedding
/ Region2Vec models on top of them. Pass `convert_tokens_to_ids(...)` output into
the geniml model; do not train embeddings inside gtars.

```python
from gtars.tokenizers import Tokenizer
from gtars.models import RegionSet

tokenizer = Tokenizer.from_bed("universe.bed")
ids = tokenizer.convert_tokens_to_ids(tokenizer.tokenize(RegionSet("training.bed")))
# -> feed `ids` to a geniml or custom model (vocab_size = tokenizer.vocab_size)
```

## Performance considerations

- Build the tokenizer once and reuse it; vocabulary construction is the costly step.
- Tokenize whole `RegionSet`s in one call rather than region-by-region.
- Persist token IDs with `gtars.utils.write_tokens_to_gtok` to avoid re-tokenizing.
