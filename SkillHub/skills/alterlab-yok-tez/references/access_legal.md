# Access model and legal basis

Source: tr:yok-tez research findings (pre-verified) + key_resources legal cites +
the verified İzinli/İzinsiz definitions from the live site (2026-06-06). Set
correct expectations with the user; do not over-claim.

## İzinli vs. İzinsiz (the permission status)

| Status | Meaning | What you can access |
|--------|---------|---------------------|
| **İzinli** (permitted) | Author authorized full-text access | Full text, **online-view-only** (browser, no photocopy / bulk download) + all metadata + *özet* (abstract) |
| **İzinsiz** (restricted) | No publication permission | **Metadata + *özet* (abstract) only.** Full text reachable in print via **TÜBESS** / inter-library loan through a university library |

**Abstracts (*özet*) are always available**, even when the full text is
embargoed. This is why an originality check must include İzinsiz theses
(`permission_status = Tümü`): the abstract alone establishes prior art.

`get_yok_tez_document_markdown` (the full-text→Markdown tool) works **only on
İzinli theses**.

## Pre-2006 closed theses

Theses closed before 2006 can be **opened by the author** by submitting a
***Tez Yayımlama İzin Belgesi*** (thesis-publication permission document) to YÖK,
after which the full text becomes accessible.

## Legal basis

- **Law 7100, Art. 10** and **Higher Education Law 2547, Additional Art. 40** —
  theses are made **electronically accessible by default** unless an authorized
  *gizlilik* (confidentiality) decision is imposed.
- **No fixed maximum embargo length.** YÖK's FAQ gives no official maximum
  embargo duration. **Do not assert a "12-month cap"** or any specific ceiling —
  it is not stated in the source.

## Scope boundary

Registry coverage from this skill answers *"does a thesis on this topic exist /
is it registered?"* It is **not**:

- a **text-similarity / plagiarism score** — that is iThenticate / Turnitin
  territory, out of scope here;
- a **quality or novelty judgment** of the student's contribution — the
  supervisor makes that call from the surfaced prior art.

Always frame originality-check output as *"here is the registered prior art;
you judge novelty"*, never as an automated originality verdict.
