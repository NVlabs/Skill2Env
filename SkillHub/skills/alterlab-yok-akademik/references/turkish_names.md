# Turkish name normalization for YOK Akademik matching

Turkish-character handling is a **first-class correctness concern** here: a naive
ASCII fold silently misses the right academic, and Turkish casing is not the same as
the default Unicode/ASCII casing.

## The dotted/dotless I trap

Turkish has **two** letter I's, and they do not map the way ASCII expects:

| Upper | Lower | Note |
|-------|-------|------|
| `İ` (dotted, U+0130) | `i` | uppercase of ASCII `i` in Turkish |
| `I` (dotless, U+0049) | `ı` (U+0131) | uppercase of dotless `ı` |

So a locale-naive `"İLKER".lower()` can yield `"i̇lker"` (with a combining dot) and
`"ışık".upper()` yields `"IŞIK"`, not `"IŞIK"` the way ASCII would. **Do not rely on
`str.lower()/upper()` for matching.** Use explicit character maps.

## The six diacritic pairs

`Ç/ç  Ğ/ğ  İ/i  I/ı  Ö/ö  Ş/ş  Ü/ü`

(Ğ/ğ never starts a word.) Users type these inconsistently — `"Çağrı"`, `"Cagri"`,
`"Cağri"` all refer to the same person, and a foreign collaborator will almost
always type the ASCII form.

## Matching strategy (what the helper does)

1. **Send the user's string as-is**, correctly UTF-8 encoded. The portal indexes the
   diacritic forms, so the exact-diacritic query is the most precise.
2. **Also try a diacritic-folded ASCII variant** of the query
   (`ç→c, ğ→g, ı→i, İ→i, ö→o, ş→s, ü→u`) so an ASCII-typed name still reaches the
   record. Merge and de-duplicate the two candidate sets.
3. **Score candidates** by comparing the *folded* form of each result's name against
   the *folded* query (a difflib-style ratio is enough), but **display the original
   diacritic name** to the user.
4. **Never auto-pick** on a name match alone — surname collisions and common names
   (Yılmaz, Demir, Şahin) are frequent. Disambiguate by institution/unvan with the
   user before asserting an affiliation.

## Fold table (canonical)

```
İ → i   I → ı   (display) / both → i (fold for matching)
Ç → c   ç → c
Ğ → g   ğ → g
Ö → o   ö → o
Ş → s   ş → s
Ü → u   ü → u
```

For matching only, fold to lowercase ASCII; for **display**, always preserve the
original diacritics in user-facing strings (proper Turkish spelling).
