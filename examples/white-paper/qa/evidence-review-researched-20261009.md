# Independent researched-evidence review — white paper

- Reviewer: gpt-6-sol, high reasoning, independent agent; 2026-10-09.
- Reviewed canonical `report.md` SHA-256: `98CF82370CA33BAFD8C5CED6B2DF60C9620D09D517853E11AD5DDE9702F00BB2`.
- Scope: commission and reader brief; the whole manuscript; `evidence/sources.json`, `claims.json`, `links.json`, and `numbers.json`; original local archives S01, S02, S03, S07, and S11 (not merely the register excerpts); the live primary [Digital.gov principles](https://digital.gov/guides/plain-language/principles/), [Digital.gov paraphrase-testing page](https://digital.gov/guides/plain-language/test/paraphrase-testing), [NASA requirements-management §6.2](https://www.nasa.gov/reference/6-2-requirements-management/), and [Gao et al. 2023 ALCE abstract](https://aclanthology.org/2023.emnlp-main.398/). The S12–S15 local extracts are selective; the live pages above were checked as the external originals. This was a semantic source-fit and completeness review, not a PDF visual review or a new effectiveness experiment.

## Verdict

**Revise before binding as a passing evidence review.** The external rationale is accurately bounded overall, but the evaluation paragraph leaves out material initial failures, and one design instruction is worded as an achieved effect. The register also misses a consequential evaluation-boundary statement.

## Located findings

1. **Material counterevidence omitted — “What has actually been demonstrated.”** S03, “Actual executions,” reports initial material issues in W01 (release version set unclear), W02 (task/repetition breadth and allocation to engineering families unclear), and W04 (assigned writing instructions described as shared raw-input evidence). W03 had no demonstrated material factual or comprehension defect. The manuscript reports only final agent passes after correction and revision. A reader could infer that the original outputs passed or that the sole problem was the later source correction. State briefly that three of four initial cases had these reviewer/reader defects, later repaired. If calling the cases a comparison, S03 also clarifies that the executive pair was direct versus managed compact, while the technical pair was full versus compact; do not imply a single full-versus-compact design across both audiences. This finding changes the evaluation's balance, not the fact that the final reviews passed.
2. **Mechanism stated as demonstrated efficacy — “What the workflow adds,” C04.** “A separate editing pass fixes located reading problems while preserving the claim's scope” is linked to S11, “Located prose-editing pass,” which instructs an editor to do this but supplies no measured result. The manuscript later correctly says the editing instructions were not tested in the comparison. Use design wording such as “targets located reading problems and checks that the claim's scope is preserved.” Recheck C04's claim text and link relation after revision.
3. **Unregistered consequential boundary — final evaluation paragraph.** “The later prose-editing instructions were not tested in that comparison, which delivered Markdown; this PDF is a separate demonstration” materially limits the apparent evidence for this finalized skill and PDF output. It is supported by S03 “Changes and use cases”/“Interpretation and limits” and S11's later instruction, but it has no emitted claim in `claims.json` and no passage link. Register the bounded statement and its support. The report's graph threshold is also not covered by the exact C02 excerpt, though S01/S02 support the adjacent cited prose; check coverage when updating the ledger.

## Claims that withstand the source check

Digital.gov supports audience-matched language and upfront organization (principles, “Choose your words carefully” and “Follow plain language guidelines”); its paraphrase-testing page asks human participants to restate meaning without interviewer correction. The report appropriately calls an agent reader a preliminary check. NASA §6.2.1.2.2–.4 supports traceability, review of the correctness of a requirements trace, and change-impact assessment; applying this to paper claims is clearly labeled an engineering analogy. ALCE's 2023 abstract separates fluency, correctness, and citation quality and reports incomplete citation support in its tested setting; the report does not project a 2023 benchmark rate onto current models or this skill. The hypothetical test-log example and the proposed failure audits are presented as examples/applications rather than observed trials. S03 and S06 support four initial author cases, four revision episodes, final 4/4 independent semantic and fresh-reader outcomes, and the stated limits. The report correctly avoids quality, cost, or human-comprehension claims from structural control tests. No conflicting primary-source passage or unsupported numerical value was found in the current text.

## Limits of this review

The local archives establish design and reported project outcomes, not independent replication. I did not re-run the historical author cases, re-interview human readers, inspect the PDF pages, or certify every implementation detail. My verdict is tied to the manuscript hash above; any revised manuscript needs a fresh evidence check and new review binding.

## Targeted recheck — 2026-10-09

- Revised `report.md` SHA-256 at this check: `493035FC6E9521B2F2C381CA66E1B7764312015B495A08B19AD42AC8AA7E57E3`.
- Finding 1 **resolved in manuscript and register**: the evaluation now discloses three initial drafts requiring attribution/scope correction before final passes. S03 “Actual executions” names W01, W02, and W04 and supports the compressed summary. C13/E13 register the statement; the wording does not claim a uniform full-versus-compact comparison.
- Finding 2 **resolved**: C04 and the report now describe the editing pass as targeting located problems and checking scope, which matches S11's instruction without claiming measured efficacy.
- Finding 3 **partly resolved**: C14/E14 register the full-graph threshold and match S01 “Start or resume.” C15 registers the evaluation boundary, but E15 is not yet a valid passage link. Its excerpt, “The prose-editing instruction was revised after the comparison,” does not occur in original S03 at the cited “Changes and use cases / Interpretation and limits” locator. S03 supports Markdown-only historical delivery, while S11 documents the current pass but does not date it against the trial. An exact source passage or a separate chronology record is needed for “later”/“not tested”; otherwise narrow the claim and link to what the originals establish.

**Current verdict: conditional revision required for E15's source fit.** All other changed support checked out. Rebind only after that link/claim is corrected and rechecked against the then-current manuscript and registers.

## Final bounded-claim recheck — 2026-10-09

- Final reviewed `report.md` SHA-256: `6035F995EFA0BD866498A6088AA3E2321649E25058683D6A1E5D31EE842E069F`.
- C15/E15 now state only that the comparison delivered Markdown, cannot establish PDF layout quality, and that the present PDF is a separate demonstration. Original S03 “Interpretation and limits” contains E15's exact excerpt: “Markdown-only cases do not establish rendered PDF/Word quality.” The current PDF artifact is present. The unsupported editing chronology has been removed.
- C13/E13 still disclose and support the three initial material problems; C04/E04 remain framed as a design check, not measured benefit; C14/E14 still match the original full-graph threshold. No new unsupported claim or material counterevidence gap was introduced by these edits.
- Minor citation precision: `[@S11]` remains at the end of the evaluation paragraph although that paragraph now relies on S03 alone. It can be removed without changing the evidence conclusion.

**Final evidence verdict: pass for the hash above, with the nonblocking citation cleanup noted.** This is a semantic source-fit/completeness verdict, not a visual PDF review or a claim of general effectiveness. Earlier conditional verdicts in this note document prior versions only.

## Citation-only final check — 2026-10-09

- Current `report.md` SHA-256: `3EA34CD58987654DA0762A12D0C6FE8CE172D4ACEB4CF78CBD8DF9A495D950E6`.
- Verified that the evaluation paragraph now ends with `[@S03]`; the redundant `[@S11]` citation was removed. The substantive evaluation wording and the supporting C15/E15 boundary remain as reviewed above. The executive report remains at SHA-256 `DDD209F5AD658E3563F59FB38B1FAA730D065751489835C7554E11B555EAAACE`.

**Current final evidence verdict: pass for the white-paper hash immediately above.** No open evidence finding remains in the reviewed text. This note does not bind a journal review or cover visual PDF QA.
