# Search craft — stemming, boolean operators, TR+EN pairing

Source: tr:yok-tez research findings (pre-verified) + the verified Detaylı Tarama
field labels. These rules turn a plain topic into a precise query the agent
constructs automatically.

## 1. Turkish auto-stemming → search roots, not inflected forms

The search engine auto-stems Turkish. Querying an inflected/suffixed form
narrows the match unnecessarily, so reduce to the **root**:

| User concept | Query this (root) | Not this (inflected) |
|--------------|-------------------|----------------------|
| sürdürülebilirliğin | `sürdürülebilir` | `sürdürülebilirliğin` |
| dijitalleşmenin | `dijital` / `dijitalleş` | `dijitalleşmenin` |
| üretkenliğe | `üret` / `üretken` | `üretkenliğe` |

Diacritics (ç ğ ı İ ö ş ü) do **not** need to be normalized by the user — the
engine handles them. Keep proper Turkish spelling in user-facing strings.

## 2. Boolean operators are Turkish words

Use **`ve`** / **`veya`** / **`içermesin`**, not `AND` / `OR` / `NOT`:

| Logic | Operator | Example |
|-------|----------|---------|
| AND | `ve` | `sanal prodüksiyon ve sinema` |
| OR | `veya` | `sanal prodüksiyon veya virtual production` |
| NOT (must-not-contain) | `içermesin` | `prodüksiyon içermesin tiyatro` |

**Phrase match** by keeping the words adjacent (no special quote syntax
required); spacing words groups them as a phrase.

## 3. Always run BOTH a Turkish AND an English query

English search terms only match the **English** title/abstract/keyword fields a
thesis provides; Turkish terms only match the Turkish fields. A thesis written
or indexed in English is **silently missed** by an all-Turkish query, and
vice-versa. So for any topic:

1. Run query A in Turkish (`Konu` + `Tez Adı` + `Özet`).
2. Run query B with the English equivalents.
3. Merge and dedupe on `Tez No`.

Generating the TR↔EN synonym set is a good local-LLM (qwen3-coder / gemma4)
offload.

## 4. Target the right fields

A title may not name the concept its abstract develops, so cover all three:

- **`Konu` (subject_headings)** — controlled subject categories.
- **`Tez Adı` (thesis_title)** — exact-ish title hits.
- **`Özet` (abstract_text)** — recall booster; catches concepts absent from titles.

For author/advisor discovery use **`Yazar` (author_name)** /
**`Danışman` (advisor_name)** — note Turkish-name diacritic variants (İ/ı, Ş/ş,
Ğ/ğ, Ç/ç, Ö/ö, Ü/ü); normalize candidate names when matching results.

## 5. Worked example (originality check)

> "A student wants to do a doctorate on *virtual production in cinema*. Has it
> been done in Turkey?"

```
Query A (TR):  Konu/Tez Adı/Özet = "sanal prodüksiyon" ve "sinema"
Query B (EN):  Konu/Tez Adı/Özet = "virtual production" ve "film"
thesis_type   = Doktora
year_start    = 2015   year_end = 2026   (if the user gave a window)
permission_status = Tümü   # include İzinsiz/restricted — they are still prior art
```

Merge A+B, dedupe on `Tez No`, return newest-first
`{Tez No, year, university, danışman, title, izin}`.
