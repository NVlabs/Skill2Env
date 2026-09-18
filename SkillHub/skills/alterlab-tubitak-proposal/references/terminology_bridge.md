# Terminology Bridge — International ↔ TÜBİTAK

Researchers often arrive with NSF/NIH/ERC-shaped material. Translate the **concept** into the
TÜBİTAK form's heading, do not transliterate word-for-word, and do not bolt international section
names onto a Turkish form. Generic grant-craft (argumentation quality, Gantt rendering, narrative
polish) stays with `alterlab-research-grants`; this glossary only fixes the *mapping*.

| International framing | TÜBİTAK term (form heading) | Where it lives | Drafting note |
|-----------------------|-----------------------------|----------------|----------------|
| Significance / intellectual merit / innovation / "what is new" | **Özgün değer** | §1 (esp. 1.1) | The single most weighted axis; name the gap and the new contribution explicitly |
| Specific aims | **Amaç ve Hedefler** | §1.3 | One amaç (aim); several **measurable** hedefler tied to work packages |
| Hypothesis / research question | **Araştırma Sorusu / Hipotezi** | §1.2 | Falsifiable, sharp, tied to the aim |
| Approach / research design / methods | **Yöntem** | §2 | Carries appropriateness *and* feasibility |
| Feasibility | **Yapılabilirlik** | §2 + §3 | Split: method can answer (§2) vs plan can execute (§3) |
| Work packages / Gantt chart | **İş Paketleri / İş-Zaman Çizelgesi** | §3.1 | Gantt aesthetics → `alterlab-research-grants` |
| Risk / contingency / mitigation plan | **B-Planı** | §3.1 | **Required** sub-element, not optional |
| Facilities & resources | **Araştırma Olanakları** | §3.2 | Infrastructure, equipment, collaborator resources |
| Broader impacts | **Yaygın etki** | §4 | Split into çıktılar / etkiler / bilim iletişimi |
| Expected outcomes / deliverables | **Öngörülen Çıktılar** | §4.1 | Publications, theses, datasets, software, patents |
| Impact (economic/societal/scientific) | **Öngörülen Etkiler** | §4.2 | Be concrete; avoid generic "will benefit society" |
| Dissemination / outreach / sci-comm | **Bilim İletişimi / Yayılım** | §4 | How results reach the field and the public |
| References / bibliography | **Kaynaklar** | EK-1 | Verify existence with `alterlab-citation-verifier` |
| Budget justification | **Bütçe ve Gerekçesi** | EK-2 | Every line tied to a work package |
| Data-management plan (DMP) | **Veri Yönetim Planı (VYP)** | (compliance) | Route to `alterlab-kvkk-dmp` / `alterlab-aperta` — not drafted here |
| IRB / ethics approval | **Etik Kurul onayı** | (compliance) | Route to `alterlab-tr-research-ethics` |

## Pitfalls when porting international proposals

- **Don't lead özet with broader impacts.** TÜBİTAK reads özgün değer first; put the novel
  contribution up front, then aim, method, impact.
- **Don't drop the B-Planı.** US forms often fold risk into "approach"; TÜBİTAK expects an explicit
  contingency plan inside the work-package section.
- **Don't merge yaygın etki into one paragraph.** The form expects three distinct sub-parts.
- **Don't carry over the page/word conventions.** TÜBİTAK enforces a 600-word özet (each language)
  and, for 1002-A, a 12-page form — see `program_profiles.md`.
- **Don't translate "broader impacts" as a literal phrase.** The functional equivalent is
  *yaygın etki*, structured differently.
