# ALL KONJAC website

## Buyer resources and quotation examples (2026-10-22)

The four business pages use `source/buyer-briefs.json` and `source/data/buyer-resources.json` for localized procurement references, selectable enquiry templates and contextual WhatsApp/email links. Clipboard support is progressive; no form, sending backend or new click analytics is installed. The internal manual enquiry workflow is `audits/enquiry-ledger.md`.

Three anonymous quotation PDFs and their HTML summaries share `source/data/quotation-sample.json`. These are illustrative amounts and clauses, not live prices or completed-sale evidence. Source identity and the original document are excluded. To regenerate PDFs, run `python scripts/prepare_quotation_print.py`, serve the checkout locally, and run `scripts/export_quotation_pdf.cjs` with the preview URL and Playwright module configured. Chromium is used for correct Thai text shaping with the existing licensed local font. Inspect every PDF page after regeneration. Do not use the historical supplier-update value as a batch COA result.

Publication now uses an explicit package: after building and checking, run `python scripts/package_public.py`, then Wrangler dry-run/deploy with `wrangler.jsonc`. Its asset directory is `.wrangler/public`, containing only the 39 canonical pages, 404, discovery files and approved public assets (106 files for this release). Internal directories and original customer files are never copied into that package. The Worker sets `X-Robots-Tag: noindex` on the three sample PDFs while keeping their explanatory HTML pages indexable. Do not deploy until the package is current.

Six article reading routes distinguish purchasing, material comparison, measurement, application research, food-equipment scope and dried-chip planning. All three languages contain the same routes; publication dates are preserved and the substantive reading-route update is dated 2026-10-21. Thai and Indonesian remain editorial drafts pending native industry review.

## External editorial citations

`audits/external-citations-2026-10-19.md` identifies the currently live pages suitable for fact-checked editorial references. The shared process is in `../link-development-2026-10-19.md`. These are internal operating documents excluded from deployment; no link quotas, anchor ratios, paid ranking links or automated placements are part of the site build.

## Three-language KGM journal (2026-10-20)

The English `/blog/` index and two KGM research articles are maintained in `source/kgm-blog/`. Three English buyer guides are maintained in `source/blog/articles.json`, with first-party claim records in `source/blog/evidence.json`. Thai and Indonesian Blog copy is in `source/blog/localized.json`; `scripts/localized_blog.py` renders those twelve pages. Run `python scripts/build.py` to generate all 21 Blog pages, 15 business pages and 3 COA reference pages. Each language has Blog navigation, reciprocal language links, canonical URLs, and sitemap entries. Research citations, study limitations, and buyer-guide source scope must remain visible. Thai and Indonesian editorial drafts still require native industry review.

`source/buyer-briefs.json` supplies the four business-line enquiry briefs in all three languages. These distinguish buyer inputs, documents to discuss, decision boundaries and next steps. WhatsApp and email links carry business-line context; clicks are intent signals rather than qualified leads. The internal baseline, 24-question AI observation set, photo provenance gaps and post-release checks are in `audits/seo-geo-release-2026-10-20.md`.

## Approved images retained (2026-10-21)

The unified release restores the previously approved image files from the 2026-10-16 release, including the ALL KONJAC watermark at 10% opacity and approximately one-third of the prior pattern density. No images are regenerated during this integration. Original photos, QR images and approved material visualizations remain unchanged. The source inventory records the historical transformations and hashes; `python scripts/check_watermarks.py` verifies the approved outputs.

Material visuals do not establish measured particle size, whiteness, species, performance or project ownership. Keep original source documents and ownership records outside the deployed asset directory.

## Unified release source

Use the current `origin/main` as the base for future production changes. Merge approved work before deployment; do not deploy an older worktree over this integrated release. The canonical inventory is 39 URLs: five business pages, six articles, one Blog index and one COA reference page per language. `python scripts/build.py --check` must pass before rendering and publication.

The comparison article and translations are in `source/comparison/`. The shared numerical quality data are in `source/data/coa-reference-en.json`; stored Thai and Indonesian quality strings are in `source/data/quality-translations.json`. Google translation preparation is a separate, optional operation; normal builds have no network dependency. Translation drafts have terminology checks but are not represented as native industry-reviewed copy.

The quality pages distinguish historical sample report results from a supplier-provided 93% update. They are not manufacturer-issued batch COAs. Preserve the 17 report rows and one supplier-update row, and never turn a quantitation limit into a measured concentration or conformity claim.

## Interactive equipment exterior view (2026-10-12)

The English, Thai and Indonesian drying-line pages share an exterior 3D reference visualization. The equipment pages no longer embed it. The viewer loads automatically and gently rotates while in view. Leaving the section or switching browser tabs pauses drawing and rotation; returning resumes the visitor's selected rotation state. Reduced-motion preferences start still. Dragging, view presets and zoom allow closer inspection, with accessible pause/reset controls and keyboard rotation. Unsupported WebGL falls back to the equipment image.

This model is an exterior visualization with relative proportions. It does not define the dimensions, rating, exact configuration or internal operation of any listed product. Existing reference specifications, contacts and the other business pages are maintained independently. Original videos, workshop reference photos and local source notes are excluded from public assets.

Editable UI, geometry and viewer code are in `source/data/equipment-3d-*.json` and `source/equipment3d/`. Shared section styles and initialization are in `assets/equipment-3d.css` and `assets/equipment-3d.js`. Three.js 0.180.0 and esbuild 0.25.10 are pinned for the viewer build. Supply an installed runtime containing those packages with `node scripts/build_equipment_3d.mjs --runtime <runtime-root>`, then run the normal site generator. The generated viewer assets stay committed, so production hosting still needs only the existing static asset deployment.

The loading/fallback poster follows the current approved image-watermark rules. Retain its unwatermarked original outside the repository and run `node scripts/watermark-equipment3d-poster.cjs <private-original-poster>` after regeneration; this updates only the new poster and its inventory entry. For a reviewed model revision, retain the previous original and use `--replace-reviewed-poster` to replace the inventory entry. PNG and WebP originals are supported; the public output stays WebP. `EQUIPMENT_PLAYWRIGHT_MODULE` can select an existing local Playwright installation. The live 3D rendering remains an exterior visualization and does not assign a manufacturer or reference specification.

The v003 static blade slopes downward from its outer support into the hopper. The user confirmed the direction and requested retaining the provisional 12-degree angle; it has not been measured. Blade guides, supports and a narrow wall passage follow that geometry. No cutting stroke is simulated. Whole-machine exterior acceptance remains pending. Browser verification can use `EQUIPMENT_WEBGL_BACKEND=d3d11` when the installed browser cannot initialize its SwiftShader backend.

`scripts/verify_equipment_3d.cjs --out <QA-directory>` checks automatic loading, rotation, views, input, visibility, mobile simulation and fallback behavior against a local HTTP preview. Pass `--url` or `--playwright-module` for another local runtime. Offline review exports are separate copies with `noindex,nofollow`; they are not production assets.

Static international B2B website for https://allkonjac.com/. The deployed files are ordinary HTML, CSS, JavaScript and images. No server application or cloud build step is required.

## Public pages and languages

The English URLs remain unchanged:

- `/` — overview, buyer questions and contact details
- `/ingredients/` — konjac powder, refined powder and konjac gum
- `/equipment/` — food equipment and production-line engineering
- `/drying-lines/` — konjac dried-chip drying systems
- `/technology/` — hydrocolloid formulation and application development

The same five business pages exist under `/th/` for Thai and `/id/` for Indonesian, giving 15 business pages. Language links preserve the current business page. Internal navigation stays in the selected language. All shared assets use `/assets/` URLs, including local font files.

All 15 business pages use shared motion via `body.motion-enabled`. It provides a one-time gentle scroll reveal for titles and copy, staggered business cards, subtle card hover and clipped image zoom. English, Thai and Indonesian use identical behavior. Detail images retain their dimensions and margins; navigation, language controls and the trilingual 404 remain immediately readable. Without JavaScript, IntersectionObserver support, or with reduced motion enabled, content remains fully visible. Reduced motion changes, keyboard focus and printing also reveal pending content. No third-party animation dependency is required.

The single root `404.html` provides English, Thai and Indonesian explanations and return links. It carries `noindex,follow` and is not listed in the sitemap. The existing Wrangler `not_found_handling: "404-page"` configuration provides an actual 404 response for unknown paths rather than a 200 rewrite.

## Editing and generating

Python 3.9 or later is sufficient; only the standard library is used. From the repository root:

```text
python scripts/build.py --self-test
python scripts/build.py --check
python scripts/build.py
```

`--self-test` verifies all 15 template variants, URL and schema transformations, HTML/attribute/JSON escaping, strict missing-key rejection and sitemap count in memory. It can run while translations are being prepared and writes no placeholder translation pages. `--check` validates the complete three-language site in memory. The ordinary command writes the 15 HTML files, root trilingual 404, sitemap and llms.txt only after all inputs validate. It never publishes, installs packages, or contacts a translation service.

Generator inputs:

- `source/templates/*.html` — editable page templates copied from the approved English HTML; full paragraphs and questions remain intact
- `source/schema/*.json` — structured-data templates, using objects such as `{"$t": "stable_translation_id"}` for descriptive strings
- `content/en.json`, `content/th.json`, `content/id.json` — flat JSON objects with identical stable string IDs and non-empty string values
- `source/translation-context.json` — extraction locations for translators and reviewers
- `source/original/*.html` — the five original English pages retained as a reference
- `scripts/build.py` — deterministic static generator

The initial English catalog contains 233 unique strings. Descriptive metadata, alt/aria labels, structured-data descriptions, menu labels, hero overlay and 404 text are included. Duplicate English strings share one ID. Hash-shaped IDs are stable identifiers: keep them when editing an existing string, then update all three catalogs together. Add a new unique key for a new concept or sentence. Template tokens `{{t:ID}}` escape HTML text; `{{a:ID}}` escape HTML attributes. Translations are plain text and must not contain markup. Structured data is serialized with JSON escaping and script-termination protection.

Translations must preserve ALL KONJAC, WhatsApp, WeChat, contact details, URLs and numerical facts. The generator rejects incomplete catalogs, unexpected keys, empty values and changed protected contact/brand/numerical facts. It has no English fallback. Review Thai and Indonesian drafts from Google Translate against the original English and the technical glossary before generating pages; automatic drafts do not establish product specifications or business claims.

`scripts/extract_catalog.py` is the one-time bootstrap extractor. It refuses to replace an existing catalog. Do not rerun it over generated pages; future edits belong in the source templates, structured-data templates and catalogs. Direct edits to generated HTML will be replaced on the next generation. Shared presentation and progressive navigation enhancement remain in `assets/site.css` and `assets/site.js`.

## Discovery metadata

Every business page has its own translated title/description, canonical URL, HTML language and Open Graph locale. The language alternates are reciprocal `en`, `th`, `id` and `x-default`, with `x-default` pointing to the corresponding English business page. The sitemap lists all 15 URLs and the same alternates. There is no automatic IP or browser-language redirect.

Organization and WebSite IDs remain global. Organization contact facts stay unchanged. Page, service, item-list and breadcrumb identities and page links use the corresponding language URL. WebSite `inLanguage` declares all three languages. Descriptive structured-data strings are localized and must match visible business information. No unsupported certifications, capacity, customers, founding dates or performance guarantees may be added.

`llms.txt` is a factual index linking all 15 business pages. It is optional and does not guarantee search rankings or AI citations. `robots.txt` retains the existing crawling policy and points to the sitemap. Google Search Console work and indexing actions are paused for manual review; generation does not submit URLs or change Google settings.

## Hosting and review

`wrangler.jsonc` binds root static assets to `worker.mjs`. The Worker redirects HTTP to HTTPS with status 301 while preserving path and query, and delegates HTTPS requests to the static assets binding. `.assetsignore` excludes catalogs, templates, scripts, audits, preparation material, the Worker source, dependencies and repository/deployment metadata from public assets. Keep those exclusions when changing the preparation workflow.

Before production publication, review the generated preview in all three languages and check desktop/mobile navigation, current-business-page language switching, long labels, typography, images and keyboard access. Confirm all 15 pages and assets return 200; unknown URLs must return 404. Production DNS, domain bindings and redirects remain separately managed in Cloudflare. This localization generator performs no preview or production deployment, commit, push or Google indexing action.

## Equipment image gallery (2026-10-07)

The three equipment pages share four AI-enhanced equipment images and translated captions/alt text. Original configuration, ratings and certifications are not inferred from generated pictures. The disclosure stays visible next to the gallery. Source and review records are in source/translations/equipment-gallery.json; new strings use the equipment.* namespace. The complete catalog now contains 253 strings per language.

The source template provides real full-size image links. A native dialog progressively enhances image viewing with Escape, focus restoration and backdrop dismissal. Without script or dialog support, links open the image normally. Cards share the existing one-time motion; the responsive grid uses two columns, one below 700px. Three WebP sizes (480/960/1448px) use srcset; PNG masters remain in the local project outputs and are not deployed. Images are encoded from the approved generated masters without further creative editing.

## English equipment reference configurations (2026-10-08)

The card layout was first published on the English equipment page and accepted by the user. The Thai and Indonesian equipment pages now use the same nine four-field cards and balanced overview images. Maintain records in source/data/equipment-reference-en.json, equipment-reference-th.json and equipment-reference-id.json; labels, captions and alt text are in source/translations/equipment-reference.json. scripts/equipment_reference.py validates matching counts, numeric facts and technical tokens, escapes text and keeps enquiry links in the current language. Run scripts/build.py after edits. Shared fragment slots in source/templates/equipment.html and assets/equipment-reference.css apply to the three equipment pages. Locale-specific typography preserves the accepted English layout.

Dimensions keep the supplied order; power is listed per reference configuration, not inferred as per-machine or whole-line power. Only supported material details appear in remarks; no steel grades are assumed. Incomplete units, tray thickness conflicts and uncertain equipment attribution remain excluded. Contract identities, contacts, quantities, prices, commercial terms and the source DOCX must never be committed or deployed. Existing public website contacts are maintained separately. Gallery images illustrate equipment categories, not an exact model or specification.

The equipment overview now shows four third-party market product examples grouped by Chinese brands and products offered in Thailand. Three-language copy is in `source/data/snack-examples.json`; provenance and the user's 2026-10-21 commercial-display permission confirmation are in `source/data/snack-image-provenance.json`. Original image pixels are preserved under `assets/market-snacks/`. No independent license document is held in this repository. The page states that the brands are not presented as ALL KONJAC products, customers, or equipment users. The prior equipment images remain in the lower gallery.

The new reference translations were reviewed against the accepted English page. Google Translate browser access timed out twice, so no Google-generated draft is claimed for these new strings. Method and terminology notes are in source/translations/equipment-reference-provenance.json. The earlier site's Google draft records describe their own historical translation phase. Unconfirmed technical details stay excluded in every language. Manual Google Search Console indexing remains paused.

## ALL KONJAC wordmark (2026-10-15)

The header, footer and trilingual 404 use the pure-letter ALL KONJAC outlined SVG. The small square icon contains only the letters AK. Source and license are in `assets/brand/` and `assets/fonts/Manrope-OFL.txt`. Manrope is licensed under SIL Open Font License 1.1; the website serves the font locally only for the homepage heading. Regenerate pages with `python scripts/build.py` after editing templates.

## Public language policy

All public language versions must contain no Han text or Chinese font declarations in body copy, navigation, references, metadata or styles. Preserve original raster images, including existing brand marks and QR annotations. Translate Chinese text with Google Translate into the page language, then review terminology, numerical facts and meaning. Internal Chinese manuscripts must remain excluded from static deployment. `python scripts/build.py` enforces this boundary. Comparison translation provenance is in `source/comparison/translation-review.md`.
