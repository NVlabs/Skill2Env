# Akeyless vs HashiCorp Vault Enterprise

**Category:** Secrets Management
**Buyer Persona:** Rachel Kim, Director of Platform Engineering at Veracyte (healthcare tech/genomics, ~700 employees)

---

## Scorecard -- AKEYLESS

| Dimension | Weight | Score | Weighted | Key Finding |
|-----------|--------|-------|----------|-------------|
| 1. Product Fit | 25% | 5/5 | 1.25 | SaaS-native, vaultless architecture; solves exactly the "Vault operational overhead" problem |
| 2. Integration & Technical | 15% | 5/5 | 0.75 | Native K8s injection (CSI, External Secrets, Injector), dynamic secrets, AWS integration |
| 3. Pricing & Commercial | 15% | 4/5 | 0.60 | Pay-as-you-go; 70% cost reduction claimed vs Vault; no specific ACV disclosed |
| 4. Security & Compliance | 15% | 5/5 | 0.75 | SOC 2 Type II, ISO 27001/27701, PCI DSS, HIPAA, FIPS 140-2 Level 3, post-quantum ready |
| 5. Vendor Credibility | 15% | 4/5 | 0.60 | $65M funded; customers include Wix, Dropbox, Constant Contact |
| 6. Customer Evidence | 10% | 4/5 | 0.40 | K Health (healthcare reference); Cimpress, Progress migration case studies |
| 7. Support & Success | 5% | 4/5 | 0.20 | 24/7 support, migration assistance, rapid deployment ("days" from Vault) |
| **TOTAL** | **100%** | | **4.55/5** |

**Evidence Confidence:** High | **Company Agent:** Detected + engaged

---

## Scorecard -- HASHICORP VAULT ENTERPRISE

| Dimension | Weight | Score | Weighted | Key Finding |
|-----------|--------|-------|----------|-------------|
| 1. Product Fit | 25% | 4/5 | 1.00 | Industry gold standard for secrets; but operational overhead is the exact problem buyer wants to solve |
| 2. Integration & Technical | 15% | 5/5 | 0.75 | Deep K8s integration, dynamic secrets, multi-cloud; best-in-class breadth |
| 3. Pricing & Commercial | 15% | 2/5 | 0.30 | ~$51K+ ACV for 50 clients; opaque pricing; enterprise licensing complexity; plus 1 FTE overhead |
| 4. Security & Compliance | 15% | 5/5 | 0.75 | HIPAA, SOC 2, GDPR; comprehensive audit; HSM support |
| 5. Vendor Credibility | 15% | 5/5 | 0.75 | Gold standard; now IBM-backed ($6.4B acquisition); massive ecosystem |
| 6. Customer Evidence | 10% | 5/5 | 0.50 | Industry-wide adoption; dominant market share |
| 7. Support & Success | 5% | 3/5 | 0.15 | Enterprise support available but self-hosted requires significant internal ops |
| **TOTAL** | **100%** | | **4.20/5** |

**Evidence Confidence:** Medium (no Company Agent, pricing research-based only) | **Company Agent:** Not found

---

## Comparative Summary

| Dimension | Akeyless | HashiCorp Vault Enterprise |
|-----------|----------|--------------------------|
| Composite | **4.55/5** | 4.20/5 |
| Company Agent | Detected + engaged | Not found |
| Operational Overhead | Near-zero (SaaS) | High (self-hosted clusters, unsealing, upgrades) |
| HIPAA | Yes | Yes |
| K8s Dynamic Secrets | Yes, native | Yes, gold standard |
| Pricing Model | Pay-as-you-go | Enterprise license + infra + FTE |
| Migration Path | "Days" from Vault | N/A (already using Community Edition) |

**Recommendation:** Akeyless is the better fit for Veracyte's specific situation. The entire "why now" is about eliminating Vault operational overhead, and Akeyless's SaaS model directly solves that. Both vendors have strong compliance and technical capabilities, but Akeyless eliminates the 1 FTE overhead that's driving this evaluation. HashiCorp Vault Enterprise would solve some operational issues (auto-unseal, HSM) but still requires self-hosted infrastructure management. **Advance Akeyless to demo. Keep Vault Enterprise as a fallback given its ecosystem dominance.**
