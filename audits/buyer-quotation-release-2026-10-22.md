# ALL KONJAC buyer resources and quotation release

## Scope

English, Thai and Indonesian: calibrated design/export wording, task-based homepage heading and four routes, consolidated ingredient enquiry copy, four-line procurement references, copyable enquiry templates with contextual WhatsApp/email, six differentiated article next steps, and three anonymous quotation examples with HTML summaries and PDF downloads. No form, new analytics, media outreach or search-engine submission.

The 39 canonical URLs remain unchanged. Three PDFs are additional resources with selective noindex headers; no Offer/Product-price schema is added. Existing approved images and COA values are retained. Unapproved snack previews and hbhpmy changes are excluded.

## Source and rollback

Base source: origin/main `64270f7`. Latest pre-release production version verified through Wrangler: `1507c738-e7c4-406d-8bec-a5161cff2ae0` (the previous short handoff listed an earlier version). All 102 public baseline files match the base commit; no newer public content was overwritten. Evidence: `production-before-buyer-2026-10-22.json` and `pre-buyer-deployments-2026-10-22.json`.

Rollback command, if required: run the configured Wrangler CLI with `rollback 1507c738-e7c4-406d-8bec-a5161cff2ae0 --config wrangler.jsonc`. This restores the pre-update site without the new buyer resources. Future releases start from latest origin/main and build/package again; do not deploy an older worktree.

## Pre-publication verification

- Generator self-test, build/check, 39-page static audit, reciprocal language links, canonical, schema and language policy passed.
- 32 business images and 10 exempt original images passed hash verification.
- 39 pages passed 390/1440 layouts and no-JavaScript readability; localized navigation and brand links verified.
- Buyer resources passed 15 grouped checks across all languages and business lines, including clipboard success/denial, context-preserving email/WhatsApp, no-JavaScript fallback, totals and PDF downloads. No messages were sent.
- COA and material checks passed in 360/390/768/1440 layouts; historical data and separate supplier update retained.
- Comparison articles passed 12 browser scenarios and static checks.
- 3D passed 28 checks on isolated rerun. An earlier concurrent local run failed resource connections; increasing the local preview request queue and rerunning resolved the test-environment failure without changing the viewer.
- All six PDF pages visually checked. Anonymous fields and amounts verified; original company identity, contact details, active validity and browser print artifacts absent.
- Publication package contains exactly 106 public files; internal directories are excluded by explicit staging. Worker redirect/selective noindex tests and Wrangler dry-run passed.

Reports retain some historical directory names dated 2026-10-21; final layout, packaging and 3D rerun occurred 2026-10-22. Original PDFs were authored and visually checked 2026-10-21.

## Remaining observation limits

Native Thai/Indonesian industry review is pending. No new current-grade supplier documents, legal review, delivered-project proof, live Search Console metrics, Core Web Vitals, AI citation results or received enquiries are asserted. Manual enquiry workflow: `enquiry-ledger.md`. Retain the established 2026-10-21 search baseline and observation dates 2026-11-04, 2026-12-02 and 2027-01-13, while recording this release separately on 2026-10-22. No automation was added.

## Production status

Deployed on 2026-10-22 from public-source commit `8972eb8`, synchronized to origin/main before publication. Production Worker version: `018a5b4c-ca02-435a-a597-5b9d4b493df2`.

Live verification passed: all 39 canonical pages and all 105 non-404 public files match the local release. The 106th packaged file is the 404 document, checked through unknown-path responses. Three PDFs return 200 with selective noindex headers; indexable pages do not receive those headers. HTTP redirects preserve paths and queries; unknown pages and internal source/audit/script/git paths return 404. Market-snack preview paths remain absent. Production buyer-resource checks passed all 15 groups, with zero sent messages; production 3D passed all 28 checks.

Evidence: `production-buyer-quotation-2026-10-22.json`, `buyer-production-boundaries.json`, `buyer-quotation-production-browser/report.json`, `buyer-quotation-production-3d/browser-verification.json`. These are technical and content acceptance results, not proof of improved search rankings, AI citations or valid enquiries.
