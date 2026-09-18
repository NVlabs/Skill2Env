# YÖK Atlas query recipes

Worked invocations of `scripts/yokatlas_lookup.py`. All run keyless via
`uv run --with yokatlas-py python …`. Paths below are abbreviated as
`.../yokatlas_lookup.py`; the full path is
`skills/turkish-academia/alterlab-yokatlas/scripts/yokatlas_lookup.py`.

Every command prints a JSON envelope:

```json
{ "tool": "alterlab-yokatlas/yokatlas_lookup.py", "operation": "...", "count": N, "results": [ ... ] }
```

On failure (package missing or network down) it prints
`{"error": "...", "manual_instructions": "..."}` and exits non-zero — it never
fabricates statistics.

## 1. List all universities (id + name)

```bash
uv run --with yokatlas-py python .../yokatlas_lookup.py universities
```

Use the returned `universiteId` / `universiteAdi` pairs to disambiguate a fuzzy
name before a program search.

## 2. Program search with filters

```bash
# Boğaziçi computer-engineering-type programs, SAY score type
uv run --with yokatlas-py python .../yokatlas_lookup.py search \
  --puan-turu SAY --universite "boğaziçi" --program "bilgisayar" --size 20
```

```bash
# All Tıp (medicine) programs at state universities, by minimum score
uv run --with yokatlas-py python .../yokatlas_lookup.py search \
  --puan-turu SAY --program "tıp" --universite-turu DEVLET --size 100
```

```bash
# Programs reachable for a student around success rank 50,000
uv run --with yokatlas-py python .../yokatlas_lookup.py search \
  --puan-turu EA --program "psikoloji" --max-basari-sirasi 50000 --size 50
```

`--puan-turu` accepts `SAY SÖZ EA DİL TYT` (diacritics preserved).
`--universite-turu` accepts `DEVLET` or `VAKIF`. `--il` filters by province.

## 3. One program by guide code (kılavuz kodu)

```bash
uv run --with yokatlas-py python .../yokatlas_lookup.py program --kod 102210277
```

Returns the program's `YearlyStats` for up to four years. Report each figure
with its `year` and `puan_turu`.

## Reporting patterns

### Program benchmarking (DEVLET vs VAKIF)

Run the same `--program` search twice with `--universite-turu DEVLET` then
`VAKIF`, then tabulate `min_puan` and `basari_sirasi` side by side for the
latest year. State the year explicitly.

### Student advising (rank in reach)

Filter with `--max-basari-sirasi <target>` to list programs whose last placed
student's rank is at or above the student's rank. Caveat in the answer that
these are **historical** ranks (latest year + three prior), not a guarantee for
the upcoming admission cycle.

### Institutional research (staff mix + fill rate)

Fetch a program by `--kod`, then report the staff counts
(`prof`/`doc`/`dou`/`ogr_gor`/`ar_gor`) and the `yerlesen`/`kontenjan` fill rate
across the available years.

## Offline / degraded behavior

If `uv` cannot resolve `yokatlas-py`, or the host is unreachable, the script
emits an `error` envelope with `manual_instructions` pointing the user to
`https://yokatlas.yok.gov.tr`. Relay that verbatim — do not infer numbers from
memory.
